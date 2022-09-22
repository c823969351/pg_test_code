from Find_PG import *
import pg_cmd
import time

ip = "10.10.10.101"
remote_addr = '/tmp/'
upgrade1_addr = r'D:\Thor_B_mrd\MRD1808_02.02.01.52.mrd'
# upgrade1_addr = r'D:\Thor_B_mrd\mrdPatternGenerator_00.00.00.54.mrd'
upgrade2_addr = r'D:\Thor_B_mrd\MRD1808_02.02.01.52.mrd'


def reboot_test(upgrade_addr):
    remote_path, filename, local_filename = pg._transferFile(
        upgrade_addr, remote_addr)
    assert pg.pg_Upgrade_list(remote_path) == filename, '升级失败'
    pg.pg_Upgrade((remote_path + filename))
    time.sleep(1)
    assert pg.pg_Upgrade_State() == 'UPDATING'
    while (pg.pg_Upgrade_Prog() != '100'):
        print('升级中')
        time.sleep(1)
        continue
    pg.pg_sys_cmd('reboot')


def reboot_check():
    while 1:
        if mrgFindGateWay() != []:
            print("重启完成")
            break
        else:
            print("启动中")
            continue


def connect_net():
    pg.open()


def main(count=0): 
    result = False
    if count <= 3:
        try:
            print('第{}次尝试连接'.format(count + 1))
            count += 1
            time.sleep(1)
            connect_net()
            result = True
        except Exception as e:
            print("---异常---：", e)
            time.sleep(1)
            main(count)
        finally:
            if result:
                print('连接成功')
    else:
        print('连接失败')


if __name__ == "__main__":
    pg = pg_cmd.ServPg(ip)
    for i in range(100):
        if i % 2 == 0:
            upgrade_addr = upgrade1_addr
        else:
            upgrade_addr = upgrade2_addr
        tm_begin = time.time()
        main()
        try:
            IDN = pg.idn()
            print(IDN)
            reboot_test(upgrade_addr)
            print("开始重启")
            time.sleep(5)
            reboot_check()
        except Exception as e:
            print("---异常---：", e)
            pg.close()
            raise Exception("测试失败---2")
        print("测试时间")
        print("第%s次升级" % i)
        print(time.time() - tm_begin)
    pg.close()