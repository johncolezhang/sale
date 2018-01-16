from splinter.browser import Browser
from time import sleep


class Buy_Tickets(object):
    # 定义实例属性，初始化
    def __init__(self, username, passwd, order, passengers, dtime, starts, ends, seat, person):
        self.seat = seat
        self.person = person
        self.username = username
        self.passwd = passwd
        # 车次，0代表所有车次，依次从上到下，1代表所有车次，依次类推
        self.order = order
        # 乘客名
        self.passengers = passengers
        # 起始地和终点
        self.starts = starts
        self.ends = ends
        # 日期
        self.dtime = dtime
        # self.xb = xb
        # self.pz = pz
        self.login_url = 'https://kyfw.12306.cn/otn/login/init'
        self.initMy_url = 'https://kyfw.12306.cn/otn/index/initMy12306'
        self.ticket_url = 'https://kyfw.12306.cn/otn/leftTicket/init'
        self.driver_name = 'chrome'
        self.executable_path = '/Users/johncole/tool/chromedriver'

    # 登录功能实现
    def login(self):
        self.driver.visit(self.login_url)
        self.driver.fill('loginUserDTO.user_name', self.username)
        # sleep(1)
        self.driver.fill('userDTO.password', self.passwd)
        # sleep(1)
        print('请输入验证码...')
        while True:
            if self.driver.url != self.initMy_url:
                sleep(3)
            else:
                break

    # 买票功能实现
    def start_buy(self):
        self.driver = Browser(driver_name=self.driver_name, executable_path=self.executable_path)
        # 窗口大小的操作
        self.driver.driver.set_window_size(1000, 800)
        self.login()
        self.driver.visit(self.ticket_url)
        sleep(3)
        try:
            print('开始购票...')
            # 加载查询信息
            self.driver.cookies.add({"_jc_save_fromStation": self.starts})
            self.driver.cookies.add({"_jc_save_toStation": self.ends})
            self.driver.cookies.add({"_jc_save_fromDate": self.dtime})
            self.driver.reload()
            count = 0
            if self.order != 0:
                while self.driver.url == self.ticket_url:
                    self.driver.find_by_text('查询').click()
                    sleep(3)
                    count += 1
                    print('第%d次点击查询...' % count)
                    try:
                        self.driver.find_by_text('预订')[self.order - 1].click()
                        sleep(3)
                    except Exception as e:
                        print(e)
                        print('预订失败...')
                        continue
            else:
                while self.driver.url == self.ticket_url:
                    self.driver.find_by_text('查询').click()
                    sleep(3)
                    count += 1
                    print('第%d次点击查询...' % count)
                    try:
                        for i in self.driver.find_by_text('预订'):
                            if "onclick" not in i.outer_html:
                                continue
                            else:
                                i.click()
                                sleep(3)
                    except Exception as e:
                        print(e)
                        print('预订失败...')
                        continue

            print('开始预订...')
            sleep(1)

            print('开始选择用户...')
            for p in self.passengers:
                self.driver.find_by_text(p).last.click()
                sleep(1)
            print('提交订单...')
            # sleep(1)
            # self.driver.find_by_text(self.seat).click()
            # sleep(1)
            # self.driver.find_by_text(self.person).click()
            sleep(1)
            self.driver.find_by_id('submitOrder_id').click()
            sleep(1)
            print('确认选座...')
            # self.driver.find_by_id('qr_submit_id').click()
            print('预订成功...')
            sleep(1000)
        except Exception as e:
            print(e)


    def add_passengers(self, name):
        self.driver = Browser(driver_name=self.driver_name, executable_path=self.executable_path)
        self.add_name = name



if __name__ == '__main__':
    username = '1148697133@qq.com'
    password = 'w913126'

    area = {
        'shenzhen': '%u6DF1%u5733%2CSZQ',
        'changsha': '%u957F%u6C99%2CCSQ',
        'kunming': '%u6606%u660E%2CKMM',
        'xuzhou': '%u5F90%u5DDE%2CXCH'
    }
    name = ['李强', '陈歌']
    order = 0
    passengers = [name[1]]
    dtime = '2018-02-14'
    starts = area['shenzhen']
    ends = area['xuzhou']

    seat_level = ['二等座']
    person_level = ['成人票']

    Buy_Tickets(username, password, order, passengers, dtime, starts, ends, seat_level, person_level).start_buy()
