import pg_cmd
ip = "10.10.10.10"
file_name = "white.bmp"
file_path = r"D:\pattern"
window_path='{file_path}\\{file_name}' .format(file_path = file_path ,file_name = file_name)

def display_local():
    pg = pg_cmd.ServPg(ip)
    pg.open()
    pg.dispOn("ON")
    pg.displayFile(window_path,file_name) #传入路径和图片名
    pg.close()


if __name__ == "__main__":
    display_local()