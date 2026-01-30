# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest


class AppDynamicsJob(unittest.TestCase):
    def setUp(self):
        # AppDynamics will automatically override this web driver
        # as documented in https://docs.appdynamics.com/display/PRO44/Write+Your+First+Script
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.baidu.com/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_app_dynamics_job(self):
        driver = self.driver
        driver.get(
            "https://credit.yn.gov.cn/el.html?c=2fIIrxi5fxK#/form?ssc=2fIIrxi5fxK&useData=1742990588087"
        )
        driver.find_element_by_xpath(
            "//div[@id='is_jrjgzf']/div[2]/div/div/div/div/div/div/div[2]/span"
        ).click()
        driver.find_element_by_xpath(
            "//div[@id='61912af3-d56d-4188-dadb-9703c0d539c3']/ul/li[2]"
        ).click()
        driver.find_element_by_xpath(
            "//div[@id='jrjg_name']/div[2]/div/div/div/div/div/div"
        ).click()
        driver.find_element_by_xpath(
            "//div[@id='977d4f65-e10e-42d4-9703-4e2913da6247']/ul/li[9]/span"
        ).click()
        driver.find_element_by_xpath(
            "//div[@id='zf_name']/div[2]/div/div/div/input"
        ).click()
        driver.find_element_by_xpath(
            "//div[@id='zf_name']/div[2]/div/div/div/input"
        ).clear()
        driver.find_element_by_xpath(
            "//div[@id='zf_name']/div[2]/div/div/div/input"
        ).send_keys("李强")
        driver.find_element_by_xpath(
            "//div[@id='zf_time']/div[2]/div/div/div/span/div/input"
        ).click()
        driver.find_element_by_link_text("今天").click()
        driver.find_element_by_xpath(
            "//div[@id='qygthnm_ztlb']/div[2]/div/div/div/div/div/div"
        ).click()
        driver.find_element_by_xpath(
            "//div[@id='9b794fa1-4681-4d83-fca4-a1f2a6371d48']/ul/li[2]"
        ).click()
        driver.find_element_by_xpath(
            "//div[@id='id_1745291391588']/div/div/div"
        ).click()
        driver.find_element_by_xpath(
            "//div[@id='be1a4667-cdf0-4ba3-f5b8-19ddf0e157f8']/ul/li[2]"
        ).click()
        driver.find_element_by_xpath(
            "//div[@id='id_1745291391590']/div/div/div/div"
        ).click()
        driver.find_element_by_xpath(
            "//div[@id='55486b77-05ed-4623-8e0b-065facde6b97']/ul/li[8]"
        ).click()
        driver.find_element_by_xpath(
            "//div[@id='sjjyxx_daaress']/div[2]/div/div/div/div/textarea"
        ).click()
        driver.find_element_by_xpath(
            "//div[@id='sjjyxx_daaress']/div[2]/div/div/div/div/textarea"
        ).clear()
        driver.find_element_by_xpath(
            "//div[@id='sjjyxx_daaress']/div[2]/div/div/div/div/textarea"
        ).send_keys("111111")
        driver.find_element_by_xpath(
            "//div[@id='uname']/div[2]/div/div/div/input"
        ).click()
        driver.find_element_by_xpath(
            "//div[@id='uname']/div[2]/div/div/div/input"
        ).clear()
        driver.find_element_by_xpath(
            "//div[@id='uname']/div[2]/div/div/div/input"
        ).send_keys("111111")
        driver.find_element_by_xpath(
            "//div[@id='legal_phone']/div[2]/div/div/div/input"
        ).click()
        driver.find_element_by_xpath(
            "//div[@id='legal_phone']/div[2]/div/div/div/input"
        ).clear()
        driver.find_element_by_xpath(
            "//div[@id='legal_phone']/div[2]/div/div/div/input"
        ).send_keys("111111111")
        driver.find_element_by_xpath(
            "//div[@id='uname']/div[2]/div/div/div/input"
        ).click()
        driver.find_element_by_id("uname").click()
        driver.find_element_by_xpath(
            "//div[@id='uname']/div[2]/div/div/div/input"
        ).clear()
        driver.find_element_by_xpath(
            "//div[@id='uname']/div[2]/div/div/div/input"
        ).send_keys("哈哈")
        driver.find_element_by_xpath(
            "//div[@id='legal_phone']/div[2]/div/div/div/input"
        ).click()
        driver.find_element_by_id("legal_phone").click()
        driver.find_element_by_xpath(
            "//div[@id='legal_phone']/div[2]/div/div/div/input"
        ).clear()
        driver.find_element_by_xpath(
            "//div[@id='legal_phone']/div[2]/div/div/div/input"
        ).send_keys("15287425299")
        driver.find_element_by_xpath(
            "//div[@id='app']/div/div[3]/div/div/label/span/input"
        ).click()
        driver.find_element_by_xpath("//button[@type='button']").click()

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException:
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException:
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True

    def tearDown(self):
        # To know more about the difference between verify and assert,
        # visit https://www.seleniumhq.org/docs/06_test_design_considerations.jsp#validating-results
        self.assertEqual([], self.verificationErrors)


if __name__ == "__main__":
    unittest.main()
