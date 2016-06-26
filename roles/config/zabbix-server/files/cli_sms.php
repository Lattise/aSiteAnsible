#!/usr/bin/env php
<?php

class SmsSend
{
    const COMPANY_TYPE_YIDONG = 1;//移动
    const COMPANY_TYPE_LIANTONG = 2;//联通
    const COMPANY_TYPE_DIANXIN = 3;//电信

    //短信第三方下行接口地址
    const SMS_MT_URL_YIDONG = 'http://esms2.etonenet.com/sms/mt';//移动
    const SMS_MT_URL_LIANTONG = 'http://esms3.etonenet.com/sms/mt';//联通
    const SMS_MT_URL_DIANXIN = 'http://esms4.etonenet.com/sms/mt';//电信
    const SPID = '3940';
    const SPPWD = 'wlkjsh39';
    const DC = 15;//GBK

    public function send($phone, $content)
    {
        $company_type = $this->getCompany($phone);
        if ($company_type == self::COMPANY_TYPE_LIANTONG) {
            $sms_mt_url = self::SMS_MT_URL_LIANTONG;
        } elseif ($company_type == self::COMPANY_TYPE_DIANXIN) {
            $sms_mt_url = self::SMS_MT_URL_DIANXIN;
        } else {
            $sms_mt_url = self::SMS_MT_URL_YIDONG;
        }
        $sm = bin2hex(iconv('UTF-8', 'GB2312//TRANSLIT', $content));
        $command = 'MT_REQUEST';
        if ($this->isPhone(trim($phone))) {
            $da = '86' . trim($phone);
            $params = array('command' => $command, 'spid' => self::SPID,
                'spsc' => '00',
                'sppassword' => self::SPPWD,
                'da' => $da,
                'dc' => self::DC,
                'sm' => $sm);
        } else {
            //throw new SmsException('手机号码格式错误', SmsException::CODE_PHONE_ERROR);
            throw new Exception('手机号码格式错误', 404);
        }
        $url = $sms_mt_url . '?' . http_build_query($params);

        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_HEADER, false);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, array());
        curl_setopt($ch, CURLOPT_TIMEOUT, 20);

        $body = curl_exec($ch);
        $info = curl_getinfo($ch);

        if ($info['http_code'] != 200) {
            throw new Exception('调用接口失败！', 400);
        }

        return $this->mlinkResponseToArray($body);
    }

    private function getCompany($mobile)
    {
        $number_company = self::COMPANY_TYPE_YIDONG;
        $front3 = substr($mobile, 0, 3);
        $front4 = substr($mobile, 0, 4);
        if (in_array($front3, array(133, 153, 180, 181, 189))) {
            $number_company = self::COMPANY_TYPE_DIANXIN;
        }
        if (in_array($front3, array(130, 131, 132, 145, 155, 156, 185, 186))) {
            $number_company = self::COMPANY_TYPE_LIANTONG;
        }
        if ($front4 == 1349) {
            $number_company = self::COMPANY_TYPE_DIANXIN;
        }
        return $number_company;
    }

    private function isPhone($phone)
    {
        return preg_match('/^((1[3,5,8][0-9])|(14[5,7])|(17[0,6,7,8]))\d{8}$/', $phone) == 1;
    }

    private function mlinkResponseToArray($body)
    {
        $ret = array();
        $kv = explode("&", $body);
        foreach ($kv as $item) {
            list($key, $value) = explode("=", $item);
            $ret[$key] = $value;
        }
        return $ret;
    }
}

$sms = new SmsSend();

$phone = $argv[1];
$content = $argv[2];
do{
$result = $sms->send($phone, $content);

if (isset($result['mterrcode']) && $result['mterrcode'] == '000') {
    echo 'success', PHP_EOL;
    exit(0);
} else {
    echo 'failed!', PHP_EOL;
    exit(1);
}
