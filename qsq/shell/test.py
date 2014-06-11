#!/usr/bin/python
import pexpect
foo = pexpect.spawn('scp /root/.ssh/authorized_keys workstation:/root/.ssh/',timeout=300)
foo.expect(['password: '])  
foo.sendline("123456")
foo.expect(pexpect.EOF)  
