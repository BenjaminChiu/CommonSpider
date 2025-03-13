// ==UserScript==
// @name         云平台自动化脚本
// @namespace    http://tampermonkey.net/
// @version      0.3.0.9
// @description  适用于健康云平台各类表单的数据填充
// @author       BenjaminChiu
// @license MIT
// @icon         https://ehr.scwjxx.cn/favicon.ico
// @match        *://*.scwjxx.cn/*
// @match        *://*.ruifumedical.com/*
// @match        *://*.jd.com/*
// @require      https://cdn.staticfile.org/jquery/3.5.1/jquery.min.js
// @require      https://cdnjs.cloudflare.com/ajax/libs/jquery-cookie/1.4.1/jquery.cookie.min.js
// @require      https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.10.111/pdf.js
// @downloadURL https://update.greasyfork.org/scripts/460223/%E4%BA%91%E5%B9%B3%E5%8F%B0%E8%87%AA%E5%8A%A8%E5%8C%96%E8%84%9A%E6%9C%AC.user.js
// @updateURL https://update.greasyfork.org/scripts/460223/%E4%BA%91%E5%B9%B3%E5%8F%B0%E8%87%AA%E5%8A%A8%E5%8C%96%E8%84%9A%E6%9C%AC.meta.js
// ==/UserScript==



(function ()
{
    'use strict';


    // 解决vue页面注入js修改input值，
    // 只有当接收到键盘的按键(随便哪个键盘的按键消息)，才会触发input和change事件,进而把输入框中的value赋值给预设的相关变量，到这一步才算走完整个设置value的过程。
    // 所以如果想给这类加料的输入框或者选择框用原生JS赋值，设置vlaue属性过后就必须手动触发一下input或change事件。
    // const fkVueEvent = document.createEvent('HTMLEvents');
    // fkVueEvent.initEvent("input", true, true);//如果是select选择框把"input"改成"change"
    // fkVueEvent.eventType = 'message';
    const fkVueEvent = new Event("input", {view: window, bubbles: true, cancelable: false});


    const the_final = "合理膳食，饮食清淡，吃动平衡，舒畅心态。";


    // =======Util-1====获取是高血压还是糖尿病随访==========
    function get_sickness_status()
    {
        // 为什么将高血压/糖尿病status放在全局变量位置，因为转诊函数和随访结局函数都会用到
        // 高血压为True；糖尿病为False
        let sickness_status = true;

        let sickness_div_s = $('div.header-left.right-header:first');
        for (let i = 0; i < sickness_div_s.length; i++)
        {
            if (sickness_div_s[i].innerText.includes('患者随访'))
            {
                if (sickness_div_s[i].innerText.includes('高血压'))
                    sickness_status = true;
                else if (sickness_div_s[i].innerText.includes('糖尿病'))
                    sickness_status = false;

                break;
            }
        }

        return sickness_status;
    }

    // =======Util-2====体检表中所用分辨慢病种类==========
    function get_sickness_status_for_tiJian()
    {
        let sickness_status_for_tiJian = {'lao': false, 'gxy': false, 'tyb': false};
        let sickness_div = $('#ehrJkztCol')[0];
        if (sickness_div.innerText.includes('老'))
            sickness_status_for_tiJian.lao = true;
        if (sickness_div.innerText.includes('高'))
            sickness_status_for_tiJian.gxy = true;
        if (sickness_div.innerText.includes('糖'))
            sickness_status_for_tiJian.tyb = true;

        return sickness_status_for_tiJian;
    }


    // ========Util-3====获取当前村医生===来自左上角签约信息==========
    function get_cun_doctor()
    {
        // 全局变量，容纳当前村医生
        let cun_doctor = '王祥茂';

        let button_s = $('button');
        for (let i = 0; i < button_s.length; i++)
        {
            if (button_s[i].innerText.includes('健康档案'))
                cun_doctor = button_s[i].childNodes[3].innerText
        }

        return cun_doctor;
    }

    // =========Util-4====产生体征数据==================
    function get_body_DATA(gao)
    {
        // 体征数据：体温、脉搏、呼吸频率、高压、低压
        let body_DATA = {
            'body_temperature': (Math.random() * (36.9 - 36) + 36).toFixed(1),
            'pulse_rate': Math.floor(Math.random() * (82 - 64 + 1)) + 64,
            'respiratory_rate': Math.floor(Math.random() * (20 - 16 + 1)) + 16,
            'SpO2': Math.floor(Math.random() * (98 - 96 + 1)) + 96
        }

        // 传入高血压患者
        if (gao)
        {
            body_DATA['blood_pressure_high'] = Math.floor(Math.random() * (132 - 115 + 1)) + 115;
            body_DATA['blood_pressure_low'] = Math.floor(Math.random() * (84 - 68 + 1)) + 68;
            body_DATA['blood_pressure_high_2'] = Math.floor(Math.random() * (133 - 114 + 1)) + 114;
            body_DATA['blood_pressure_low_2'] = Math.floor(Math.random() * (82 - 69 + 1)) + 69;
        }
        else
        {
            body_DATA['blood_pressure_high'] = Math.floor(Math.random() * (119 - 102 + 1)) + 102;
            body_DATA['blood_pressure_low'] = Math.floor(Math.random() * (72 - 64 + 1)) + 60;
            body_DATA['blood_pressure_high_2'] = Math.floor(Math.random() * (119 - 101 + 1)) + 100;
            body_DATA['blood_pressure_low_2'] = Math.floor(Math.random() * (71 - 62 + 1)) + 60;
        }
        return body_DATA;
    }


    // =========Function-1====体检表=============
    function tiJian()
    {
        console.log("正在使用体检表填充功能.");

        // 获取 老 高 糖 状态
        let sickness_flag = get_sickness_status_for_tiJian();
        // 外部获取 转诊的村医姓名
        let cun_doctor = get_cun_doctor();
        // 外部获取体征数据
        let body_DATA = get_body_DATA();
        let body_DATA_gao = get_body_DATA("gao")


        // 修改体检表标签
        let edit_flag = false;
        let cun_doctor_flag = false;


        let form_s = $('form');
        for (let i = 0; i < form_s.length; i++)
        {
            // 找到了目标form表单
            if (form_s[i].innerText.includes('体检日期') && form_s[i].innerText.includes('责任医生') && !edit_flag)
            {
                // 只允许修改一次
                edit_flag = true;

                // 获取所有行，并且遍历所有行
                // const tr_s = form_s[i].getElementsByTagName("tr");
                let tr_s = document.getElementsByTagName("tr");
                for (let j = 0; j < tr_s.length; j++)
                {
                    if (tr_s[j].innerText.includes("体检日期") && tr_s[j].innerText.includes("责任医生"))
                    {

                        // 责任医生 步骤一：点击下拉框
                        let div_s = tr_s[j].getElementsByTagName("div");
                        for (let k = 0; k < div_s.length; k++)
                        {
                            if ("combobox" === div_s[k].getAttribute("role"))
                            {
                                div_s[k].click();
                                break;  // 仅仅终止本轮内循环。终止目的：防止多次点击下拉框，不好看，效率底下！
                            }
                        }

                        // 责任医生 步骤二：模拟点击对应村医
                        setTimeout(function ()
                        {
                            let ul_s = $('ul[role="listbox"]');
                            for (let k = 0; k < ul_s.length; k++)
                            {
                                if (ul_s[k].innerText.includes('曹碑镇卫生院'))
                                {
                                    let li_s = ul_s[k].getElementsByTagName("li");
                                    for (let z = 0; z < li_s.length; z++)
                                    {
                                        // 关键：如果下拉列表中有村医 和 签约的村医一致，则点击该村医
                                        if (li_s[z].innerText.includes(cun_doctor) && !cun_doctor_flag
                                            && !li_s[z].innerText.includes("禁") && !li_s[z].innerText.includes("停用"))
                                        {
                                            li_s[z].click();
                                            cun_doctor_flag = true;
                                        }
                                    }
                                }
                            }
                        }, 300);

                    }
                    else if (tr_s[j].innerText.includes("体温") && tr_s[j].innerText.includes("脉率"))
                    {
                        let inputs = tr_s[j].getElementsByTagName("input");
                        inputs[0].value = body_DATA['body_temperature'].toString();
                        inputs[0].dispatchEvent(fkVueEvent);
                        inputs[1].value = body_DATA['pulse_rate'].toString();
                        inputs[1].dispatchEvent(fkVueEvent);
                    }
                    else if (tr_s[j].innerText.includes("呼吸频率") && tr_s[j].innerText.includes("左侧"))
                    {
                        let inputs = tr_s[j].getElementsByTagName("input");
                        inputs[0].value = body_DATA['respiratory_rate'].toString();
                        inputs[0].dispatchEvent(fkVueEvent);
                    }
                    else if (tr_s[j].innerText.includes("SpO2"))
                    {
                        let inputs = tr_s[j].getElementsByTagName("input");
                        inputs[0].value = body_DATA['SpO2'].toString();
                        inputs[0].dispatchEvent(fkVueEvent);
                    }


                    // ========老年人专有功能=======Start=========
                    else if ((tr_s[j].innerText.includes("老年人健康状态自我评估*") || tr_s[j].innerText.includes("老年人认知能力*")
                            || tr_s[j].innerText.includes("老年人情感状态*") || tr_s[j].innerText.includes("老年人生活自理能力自我评估"))
                        && sickness_flag['lao'])
                    {
                        let divs = tr_s[j].getElementsByTagName("div");
                        for (let k = 0; k < divs.length; k++)
                        {
                            if ((divs[k].innerText.includes('2基本满意') || divs[k].innerText.includes('1粗筛阴性') || divs[k].innerText.includes('1可自理'))
                                && !divs[k].className.includes('checked'))
                            {
                                divs[k].click();
                            }
                        }

                        setTimeout(function ()
                        {
                            let table_s = document.getElementsByClassName('ant-modal-content');
                            for (let k = 0; k < table_s.length; k++)
                            {
                                if (table_s[k].innerText.includes("老年人生活自理能力评估表"))
                                {
                                    const table_divs = table_s[k].getElementsByTagName("div")
                                    for (let z = 0; z < table_divs.length; z++)
                                    {
                                        if (table_divs[z].innerText.includes('0分') && table_divs[z].innerText.includes('独立完成')
                                            && table_divs[z].className.includes('ant-tag-checkable')
                                            && !table_divs[z].className.includes('ant-tag-checkable-checked'))
                                        {
                                            table_divs[z].click();
                                        }
                                    }
                                    const button_s = table_s[k].getElementsByTagName("button")
                                    button_s[1].click();
                                }
                            }
                        }, 400);
                    }



                    else if (tr_s[j].innerText.includes("危险因素控制"))
                    {
                        const divs = tr_s[j].getElementsByTagName("div");
                        for (let k = 0; k < divs.length; k++)
                        {
                            if ((divs[k].innerText.includes('3') || divs[k].innerText.includes('4')
                                    || divs[k].innerText.includes('6') || divs[k].innerText.includes('7'))
                                && !divs[k].className.includes('checked'))
                            {
                                divs[k].click();
                            }
                        }
                        let textarea_s = tr_s[j].getElementsByTagName("textarea");
                        textarea_s[0].value = "预防骨质疏松、预防跌倒";
                        textarea_s[0].dispatchEvent(fkVueEvent);

                        textarea_s[1].value = "流感疫苗、肺炎疫苗";
                        textarea_s[1].dispatchEvent(fkVueEvent);
                }

                    else if (tr_s[j].innerText.includes("健康摘要"))
                    {
                        let textarea_s = tr_s[j].getElementsByTagName("textarea");
                        textarea_s[0].value = the_final;
                        textarea_s[0].dispatchEvent(fkVueEvent);
                    }


                }
            }
        }


        // ====Start======第4页监听器=================
        // 解决点击第4页时，自动取消“4锻炼”按钮
        let div_s = document.getElementsByTagName("div");
        for (let i = 0; i < div_s.length; i++)
        {
            if (div_s[i].innerText === "第4页")
            {
                div_s[i].addEventListener("mousedown", function ()
                {
                    for (let j = 0; j < div_s.length; j++)
                    {
                        if (div_s[j].innerText === '4锻炼' && !div_s[j].className.includes('checked'))
                        {
                            setTimeout(function ()
                            {
                                div_s[j].click();
                            }, 1500);
                        }
                    }
                });
            }
        }
        // ====End======第4页监听器=================


    }







    // 程序入口
    document.addEventListener("keydown", function (fuckEvent)
    {
        let useFlag = false;
        const pw = "wf";
        if (fuckEvent.key === "F9")
        {
            console.log("您已按下F9，实现弹窗，StartFunction");

            let user_pw = prompt("请输入密钥");
            if (user_pw === pw)
                useFlag = true;

            if (useFlag)
            {
                let DllButton = "";

                const Pre_DllButton = "<div id='fuck.this.shit' style='font-family: SimSun,fangsong; font-weight: bold; display: block; line-height: 22px; " +
                    "text-align: center; vertical-align: center; background-color: #25ae84; cursor: pointer; margin: 1px; position: fixed; left: 0; top: 185px; width: 35px; z-index: 8888;'>";
                const Btm_DllButton = "</div>";


                const tiJian_String_2 = "<a id='tiJian_a' target='_blank' style='font-size:13px; color:#fff; display: block; height: 100%; padding: 3px 1px;'" +
                    " onmouseover=\"this.style.color='red'\" onmouseout=\"this.style.color='white'\"><p>一般<br>体检</p></a>";


                DllButton = Pre_DllButton  + tiJian_String_2 + Btm_DllButton;


                $("body").append(DllButton);


                $("#tiJian_a").click(function ()
                {
                    tiJian();
                });
            }
            else
                alert("密码错误！");


        }
    });





})();
