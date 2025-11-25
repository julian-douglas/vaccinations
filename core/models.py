from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from django.utils import timezone
import re
import json

User = get_user_model()

class Vaccine(models.Model):
    name = models.CharField(max_length=100, unique=True)
    primary_series_doses = models.PositiveSmallIntegerField(null=True, blank=True)
    recurrence_interval_years = models.FloatField(null=True, blank=True)
    booster_interval_years = models.FloatField(null=True, blank=True)
    price_per_dose = models.DecimalField(max_digits=8, decimal_places=2)
    side_effects = models.JSONField(default=list, blank=True)
    administration_route = models.CharField(max_length=10, default="IM")
    manufacturer = models.CharField(max_length=100, blank=True)
    age_min = models.FloatField(null=True, blank=True)
    age_max = models.FloatField(null=True, blank=True)
    contraindications = models.JSONField(default=list, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Branch(models.Model):
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=255)
    postcode = models.CharField(max_length=20)
    phone = models.CharField(max_length=30)
    email = models.EmailField()
    opening_hours = models.JSONField(default=list, blank=True)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name
        
    def is_24_7(self):
        """
        Detect a 24/7 schedule: any dict entry whose open is 00:00 and close is 23:59 (or 24:00),
        regardless of days string (we accept Mon-Sun, Sun-Mon, etc.).
        """
        if not isinstance(self.opening_hours, list):
            return False
        for entry in self.opening_hours:
            if isinstance(entry, dict):
                o = entry.get("open", "").strip()
                c = entry.get("close", "").strip()
                if o in ("00:00", "0:00") and c in ("23:59", "24:00"):
                    return True
        return False

    def open_until_display(self):
        """
        Return 'Open until HH:MM' for today, or 'Open 24/7' if applicable.
        """
        if self.is_24_7():
            return "Open 24/7"
        if not self.opening_hours or not isinstance(self.opening_hours, list):
            return ""
        day_names = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        today_idx = datetime.now().weekday()
        today = day_names[today_idx]

        def today_in_days(spec: str):
            # Support ranges (Mon-Fri), wrap ranges (Fri-Mon), and comma lists (Mon,Wed,Fri)
            for part in [p.strip() for p in spec.split(',') if p.strip()]:
                if '-' in part:
                    start, end = [x.strip() for x in part.split('-', 1)]
                    if start in day_names and end in day_names:
                        si, ei = day_names.index(start), day_names.index(end)
                        if si <= ei:
                            if si <= today_idx <= ei:
                                return True
                        else:  # wrap
                            if today_idx >= si or today_idx <= ei:
                                return True
                else:
                    if part == today:
                        return True
            return False

        for entry in self.opening_hours:
            if isinstance(entry, dict):
                if today_in_days(entry.get("days","")) and entry.get("close"):
                    return f"Open until {entry['close']}"
        return ""

    def status_info(self):
        """
        Returns dict: {'text': 'Open until 20:00', 'class': 'status-open'|'status-closing'|'status-closed'}
        Assumes opening_hours is list of dicts: {"days":"Mon-Fri","open":"09:00","close":"20:00"}.
        Handles wrap ranges (Fri-Mon) and 24/7 (00:00-23:59).
        """
        # 24/7
        if self.is_24_7():
            return {"text": "Open 24/7", "class": "status-open"}

        if not isinstance(self.opening_hours, list):
            return None

        day_names = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        now = timezone.localtime() if timezone.is_aware(timezone.now()) else datetime.now()
        today_idx = now.weekday()
        today = day_names[today_idx]

        def day_matches(spec: str):
            # supports "Mon-Fri", "Fri-Mon" (wrap), "Mon,Wed,Fri", single day
            for part in [p.strip() for p in spec.split(",") if p.strip()]:
                if "-" in part:
                    start, end = [x.strip() for x in part.split("-", 1)]
                    if start in day_names and end in day_names:
                        si, ei = day_names.index(start), day_names.index(end)
                        if si <= ei:
                            if si <= today_idx <= ei:
                                return True
                        else:  # wrap (e.g. Fri-Mon)
                            if today_idx >= si or today_idx <= ei:
                                return True
                else:
                    if part == today:
                        return True
            return False

        def as_dt(hhmm: str):
            try:
                h, m = hhmm.split(":")
                return now.replace(hour=int(h), minute=int(m), second=0, microsecond=0)
            except Exception:
                return None

        best = None
        for entry in self.opening_hours:
            if not isinstance(entry, dict):
                continue
            days = entry.get("days")
            o = entry.get("open")
            c = entry.get("close")
            if not (days and o and c):
                continue
            if not day_matches(days):
                continue
            open_dt = as_dt(o)
            close_dt = as_dt(c)
            if not (open_dt and close_dt):
                continue
            # Overnight span (open > close) -> treat close as next day
            if close_dt <= open_dt:
                close_dt = close_dt + timedelta(days=1)
            best = (open_dt, close_dt)
            break  # first matching block

        if not best:
            return {"text": "Closed", "class": "status-closed"}

        open_dt, close_dt = best
        # If now before opening
        if now < open_dt:
            return {"text": "Closed", "class": "status-closed"}
        # If within open window
        if open_dt <= now < close_dt:
            remaining = close_dt - now
            close_str = close_dt.strftime("%H:%M")
            if remaining <= timedelta(hours=1):
                return {"text": f"Open until {close_str}", "class": "status-closing"}
            return {"text": f"Open until {close_str}", "class": "status-open"}

        return {"text": "Closed", "class": "status-closed"}

    def get_opening_hours_display(self):
        """Process opening hours data for display"""
        if not self.opening_hours:
            return []
        
        try:
            hours_data = json.loads(self.opening_hours) if isinstance(self.opening_hours, str) else self.opening_hours
        except (json.JSONDecodeError, TypeError):
            return []
        
        processed_hours = []
        for hour_block in hours_data:
            days = hour_block.get('days', '')
            open_time = hour_block.get('open', '')
            close_time = hour_block.get('close', '')
            
            if open_time and close_time:
                processed_hours.append({
                    'days': days,
                    'open': open_time,
                    'close': close_time,
                    'is_current': self.is_current_day_period(days)
                })
        
        return processed_hours
    
    def is_current_day_period(self, days_string):
        """Check if current day falls within the given days string"""
        current_day = datetime.now().strftime('%a')  # Mon, Tue, Wed, etc.
        days_lower = days_string.lower()
        
        day_mappings = {
            'monday': 'mon', 'tuesday': 'tue', 'wednesday': 'wed', 
            'thursday': 'thu', 'friday': 'fri', 'saturday': 'sat', 'sunday': 'sun'
        }
        
        current_day_short = current_day.lower()[:3]
        
        # Handle ranges like "Mon-Fri"
        if '-' in days_lower:
            start_day, end_day = days_lower.split('-')
            start_day = start_day.strip()[:3]
            end_day = end_day.strip()[:3]
            
            day_order = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
            try:
                start_idx = day_order.index(start_day)
                end_idx = day_order.index(end_day)
                current_idx = day_order.index(current_day_short)
                
                if start_idx <= end_idx:
                    return start_idx <= current_idx <= end_idx
                else:  # Wraps around week (e.g., Sat-Mon)
                    return current_idx >= start_idx or current_idx <= end_idx
            except ValueError:
                pass
        
        # Handle specific days like "Sat", "Sun", or "Sat-Sun"
        return current_day_short in days_lower
    
    def get_formatted_address(self):
        """Return address with commas replaced by line breaks"""
        if not self.address:
            return ""
        return self.address.replace(", ", "<br>")
    
class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-datetime']

    def __str__(self):
        return f"{self.user} - {self.vaccine} @ {self.datetime:%Y-%m-%d %H:%M}"

class Dose(models.Model):
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doses')
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, blank=True, related_name='doses')
    date_administered = models.DateField()
    dose_number = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('vaccine', 'user', 'dose_number')
        ordering = ['-date_administered']

    def __str__(self):
        return f"{self.user} - {self.vaccine} dose {self.dose_number}"
