'''
Created on May 14, 2014

@author: root
'''

from django.forms.formsets import BaseFormSet
from django.forms.formsets import formset_factory
from qsq.forms import *
import pexpect

class BaseArticleFormSet(BaseFormSet):
    def add_fields(self, form, index):
        super(BaseArticleFormSet, self).add_fields(form, index)
        form.fields["my_field"] = forms.CharField()


if "__main__" == __name__:
        foo = pexpect.spawn('scp /root/.ssh/authorized_keys bhwzyjy1:/root/.ssh/')
        foo.expect(['password: '])  
        foo.sendline("123456")
        foo.expect(pexpect.EOF)
    
    
