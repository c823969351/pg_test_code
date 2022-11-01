import pg_cmd

ip = '10.10.10.15'
pg = pg_cmd.ServPg(ip)
pg.open()

if __name__ == "__main__":
    # while 1:
    #     msg= pg.query('PROJect:MEMO:READ? #H80410004,U32')
    #     print(msg)
    #     if msg[2:] == '0':
    #         print('warning')
    #         break
    pg.send('PROJect:MEMO:WRITE #H80050418,U32,#H3C0')
