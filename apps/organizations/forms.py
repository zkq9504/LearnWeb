import re
from django import forms
from operations.models import UserAsk


class AddAskForm(forms.ModelForm):
    mobile = forms.CharField(required=True, min_length=11, max_length=11)

    class Meta:
        model = UserAsk
        fields = ["name", "mobile", "course_name"]

    def clean_mobile(self):
        """验证手机号码格式是否合法"""
        mobile = self.cleaned_data["mobile"]
        regex_mobile = "^[1](([3][0-9])|([4][5-9])|([5][0-3,5-9])|([6][5,6])|([7][0-8])|([8][0-9])|([9][1,8,9]))[0-9]{8}$"
        pattern = re.compile(regex_mobile)
        if pattern.match(mobile):
            return mobile
        else:
            raise forms.ValidationError("手机号码非法，请重新输入", code="invalid_mobile")
