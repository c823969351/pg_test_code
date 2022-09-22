import Remote_ssh
from symbol import return_stmt
import PG_server

class Update_FPGA(object):

    def __init__(self,local_flle_dir = '',select_bin = ''):
        try:
            self.server = PG_server.ServPg()
            self.client = Remote_ssh.Remote(self.server._host,self.server._pw)
        except Exception as e:
            raise('err:',e)
        self.select_bin = select_bin
        self.local_flle_dir = local_flle_dir
        self.remote_dir = self.select_remote_dir()
        
        
    def select_remote_dir(self):
        if self.select_bin == 'k160':
            return '/app/res/mirror/'
        elif self.select_bin == 'ZU7':
            self.mount_boot()
            return '/root/'
        else:
            raise('error')

    def transfer(self):
        remote_path, filename, local_filename= self.server._transferFile(self.local_flle_dir,self.remote_dir,self.select_bin)
        print('远程路径:{}'.format(remote_path+filename))
        print('本地名称:{}'.format(local_filename))
    
    def mount_boot(self):
        print(self.client)
        print(self.server._host)
        print(self.server._pw)
        self.client.command('mount /dev/mmcblk1p1 /root/')
    
    def reboot(self):
        self.client.command('sync ; reboot')

if __name__ == "__main__":
    dir1 = r'C:\Users\mega\Desktop\FPGA\VBO问题\thor_ext_pro_0901_15.bin'
    dir2 = r'C:\Users\mega\Desktop\FPGA\VBO问题\BOOT0919.bin'
    app = Update_FPGA(dir2,'ZU7')
    app.transfer()
    app.reboot()



        