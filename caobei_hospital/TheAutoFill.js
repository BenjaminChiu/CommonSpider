// ==UserScript==
// @name         云平台自动化脚本
// @namespace    http://tampermonkey.net/
// @version      0.1.10
// @description  适用于健康云平台各类表单的数据填充
// @author       Benjamin Chiu.topfisherman@126.com
// @license MIT
// @icon         https://ehr.scwjxx.cn/favicon.ico
// @match        *://*.ithome.com/*
// @match        *://*.scwjxx.cn/*
// @require      https://cdn.staticfile.org/jquery/2.1.1/jquery.min.js
// @require      https://cdn.staticfile.org/jquery-cookie/1.4.1/jquery.cookie.min.js
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
    const fkVueEvent_change = new Event("change", {view: window, bubbles: true, cancelable: false});



    // ===1111====体检表======Start=========
    function tiJian()
    {
        console.log("正在使用体检表填充功能.");


        // 体检表 所需变量 start
        // 体温
        const body_temperature = (Math.random() * (36.9 - 36) + 36).toFixed(1);
        // 脉搏
        const pulse_rate = Math.floor(Math.random() * (82 - 68 + 1)) + 68;
        // 呼吸频率
        const respiratory_rate = Math.floor(Math.random() * (21 - 16 + 1)) + 16;
        // 高压
        const blood_pressure_high = Math.floor(Math.random() * (138 - 128 + 1)) + 128;
        // 低压
        const blood_pressure_low = Math.floor(Math.random() * (88 - 78 + 1)) + 78;
        // 高压
        const blood_pressure_high_2 = Math.floor(Math.random() * (138 - 129 + 1)) + 129;
        // 低压
        const blood_pressure_low_2 = Math.floor(Math.random() * (88 - 78 + 1)) + 78;
        // 血红蛋白
        const hemoglobin = Math.floor(Math.random() * (155 - 115 + 1)) + 115;
        // 白细胞
        const hemameba = (Math.random() * (10 - 4) + 4).toFixed(2);
        // 血小板
        const blood_platelet = Math.floor(Math.random() * (300 - 100 + 1)) + 100;
        // 血糖
        const blood_sugar = (Math.random() * (6 - 4) + 4).toFixed(2);
        // 高血糖 随机血糖
        const blood_sugar_high = (Math.random() * (12 - 6.2) + 6.2).toFixed(2);
        // 修改体检表标签
        let edit_flag = false;
        // 体检表 所需变量 end






        // ====Start======第4页监听器=================
        // 解决点击第4页时，自动取消“4锻炼”按钮
        const div_s  = document.getElementsByTagName("div")
        for (let i=0; i<div_s.length; i++)
        {
            if (div_s[i].innerText === "第4页")
            {
                console.log(i + "@@@@@@@@@找到第4页了" + div_s[i].innerText + "End***********");
                div_s[i].addEventListener("mousedown", function (fuckEvent)
                {
                    console.log("给第4页添加鼠标触发事件成功。")
                    for (let j=0; j<div_s.length; j++)
                    {
                        // && !div_s[j].className.includes('checked')
                        if (div_s[j].innerText === '4锻炼')
                        {
                            console.log("找到4锻炼啦，哈哈哈哈");
                            setTimeout(function ()
                            {
                                console.log("触发setTimeout");
                                div_s[j].click();
                            }, 1500);
                        }


                    }
                });
            }
        }
        // ====End======第4页监听器=================











        let form_s = $('form');
        for (let i=0; i<form_s.length; i++)
        {
            // 找到了目标form表单
            if (form_s[i].innerText.includes('体检日期') && form_s[i].innerText.includes('责任医生') && !edit_flag)
            {
                // 只允许修改一次
                edit_flag = true;

                // 获取所有行，并且遍历所有行
                // const tr_s = form_s[i].getElementsByTagName("tr");
                const tr_s = document.getElementsByTagName("tr");
                for (let j=0; j<tr_s.length; j++)
                {
                    if (tr_s[j].innerText.includes("体检日期") && tr_s[j].innerText.includes("责任医生"))
                    {
                        let inputs = tr_s[j].getElementsByTagName("input");
                        inputs[0].value = $.cookie("tiJianDate");
                        inputs[0].dispatchEvent(fkVueEvent_change);
                    }
                    else if (tr_s[j].innerText.includes("体温") && tr_s[j].innerText.includes("脉率"))
                    {
                        let inputs = tr_s[j].getElementsByTagName("input");
                        inputs[0].value = body_temperature;
                        inputs[0].dispatchEvent(fkVueEvent);
                        inputs[1].value = pulse_rate;
                        inputs[1].dispatchEvent(fkVueEvent);
                    }
                    else if (tr_s[j].innerText.includes("呼吸频率") && tr_s[j].innerText.includes("左侧"))
                    {
                        let inputs = tr_s[j].getElementsByTagName("input");
                        inputs[0].value = respiratory_rate;
                        inputs[0].dispatchEvent(fkVueEvent);
                        inputs[1].value = blood_pressure_high;
                        inputs[1].dispatchEvent(fkVueEvent);
                        inputs[2].value = blood_pressure_low;
                        inputs[2].dispatchEvent(fkVueEvent);
                    }
                    else if (tr_s[j].innerText.includes("右侧") && !tr_s[j].innerText.includes("右侧弱"))
                    {
                        console.log("我他妈进入右侧血压了！");
                        let inputs = tr_s[j].getElementsByTagName("input");
                        inputs[0].value = blood_pressure_high_2;
                        inputs[0].dispatchEvent(fkVueEvent);
                        inputs[1].value = blood_pressure_low_2;
                        inputs[1].dispatchEvent(fkVueEvent);
                        console.log("找到右侧血压栏");
                    }


                    // ========老年人专有功能=======Start=========
                    else if (tr_s[j].innerText.includes("老年人健康状态自我评估*") || tr_s[j].innerText.includes("老年人认知能力*")
                        || tr_s[j].innerText.includes("老年人情感状态*") || tr_s[j].innerText.includes("老年人生活自理能力自我评估"))
                    {
                        const divs = tr_s[j].getElementsByTagName("div");
                        for (let i = 0; i < divs.length; i++)
                        {
                            if ((divs[i].innerText.includes('2基本满意') || divs[i].innerText.includes('1粗筛阴性')
                                    || divs[i].innerText.includes('1可自理')) && !divs[i].className.includes('checked'))
                                divs[i].click();

                        }
                        console.log("老年人健康评估完成.");

                        setTimeout(function ()
                        {
                            console.log("触发老年人生活自理能力评估表.");
                            let table_s = document.getElementsByClassName('ant-modal-content');
                            for (let i=0; i<table_s.length; i++)
                            {
                                if (table_s[i].innerText.includes("老年人生活自理能力评估表"))
                                {
                                    const table_divs = table_s[i].getElementsByTagName("div")
                                    for (let j=0; j<table_divs.length; j++)
                                    {
                                        if (table_divs[j].innerText.includes('0分') && table_divs[j].innerText.includes('独立完成')
                                            && table_divs[j].className.includes('ant-tag-checkable')
                                            && !table_divs[j].className.includes('ant-tag-checkable-checked'))
                                            table_divs[j].click();
                                    }
                                    const button_s = table_s[i].getElementsByTagName("button")
                                    for (let k=0; k<button_s.length; k++)
                                    {
                                        if (button_s[k].innerText.includes('保存'))
                                            button_s[k].click();
                                    }
                                }

                            }

                        }, 600);
                    }

                    else if (tr_s[j].innerText.includes("心电图"))
                    {
                        console.log("进入心电图的操作.");
                        const divs = tr_s[j].getElementsByTagName("div");
                        for (let i = 0; i < divs.length; i++)
                        {
                            if (divs[i].innerText.includes('1正常') && !divs[i].className.includes('checked'))
                                divs[i].click();
                        }
                        // let textarea_s = tr_s[j].getElementsByTagName("textarea");
                        // textarea_s[0].value = "轻微心电左偏";
                        // textarea_s[0].dispatchEvent(fkVueEvent);
                        console.log("完成心电图的操作.");
                    }
                    else if (tr_s[j].innerText.includes("腹部B超"))
                    {
                        const divs = tr_s[j].getElementsByTagName("div");
                        for (let i = 0; i < divs.length; i++)
                        {
                            if (divs[i].innerText.includes('1正常') && !divs[i].className.includes('checked'))
                                divs[i].click();
                        }
                        // let inputs = tr_s[j].getElementsByTagName("input");
                        // inputs[0].value = "轻微心电左偏";
                        // inputs[0].dispatchEvent(fkVueEvent);
                        console.log("完成B超的操作.")
                    }
                    // ========老年人专有功能=======End===========

                    else if (tr_s[j].innerText.includes("危险因素控制"))
                    {
                        const divs = tr_s[j].getElementsByTagName("div");
                        for (let i = 0; i < divs.length; i++)
                        {
                            if ((divs[i].innerText.includes('3') || divs[i].innerText.includes('4')
                                    || divs[i].innerText.includes('6') || divs[i].innerText.includes('7'))
                                && !divs[i].className.includes('checked'))
                                divs[i].click();
                        }
                        let textarea_s = tr_s[j].getElementsByTagName("textarea");
                        textarea_s[0].value = "预防骨质疏松与跌倒";
                        textarea_s[0].dispatchEvent(fkVueEvent);

                        textarea_s[1].value = "流感疫苗、肺炎疫苗";
                        textarea_s[1].dispatchEvent(fkVueEvent);
                    }
                }
            }
        }
    }
    // ===1111====体检表======End=========

    //===2222====医养结合======Start========
    function yyjh()
    {
        console.log("正在使用体检表填充功能.");
        // 修改医养结合标志
        let edit_flag = false;

        let the_fk_iframe = document.getElementById("yyjfForm");
        let iframe_doc = the_fk_iframe.contentWindow.document;
        // 跨域获取document
        let form_s = iframe_doc.getElementsByTagName("form");
        for (let i=0; i<form_s.length; i++)
        {
            // 找到了目标form表单
            if (form_s[i].innerText.includes('床上运动'))
            {
                // 只允许修改一次
                edit_flag = true;

                console.log("找到医养结合form，牛逼.");

                const div_row_s = form_s[i].getElementsByTagName("div");
                for (let j=0; j<div_row_s.length; j++)
                {
                    if (div_row_s[j].innerText.includes("服务日期") && div_row_s[j].className === "ant-row")
                    {
                        let inputs = div_row_s[j].getElementsByTagName("input");
                        inputs[0].value = $.cookie("tiJianDate");
                        inputs[0].dispatchEvent(fkVueEvent_change);
                    }
                    else if (div_row_s[j].innerText.includes("服务方式") && div_row_s[j].className === "ant-row")
                    {
                        let lable_s = div_row_s[j].getElementsByTagName("label");
                        for (let k = 0; k < lable_s.length; k++)
                        {
                            if (lable_s[k].innerText.includes('门诊') && !lable_s[k].className.includes('checked'))
                                lable_s[k].click();
                        }
                    }
                    else if (div_row_s[j].innerText.includes("健康情况") && div_row_s[j].className === "ant-row")
                    {
                        let lable_s = div_row_s[j].getElementsByTagName("label");
                        for (let k = 0; k < lable_s.length; k++)
                        {
                            if (lable_s[k].innerText.includes('无') && !lable_s[k].className.includes('checked'))
                                lable_s[k].click();
                        }
                    }
                    else if (div_row_s[j].innerText.includes("服务内容记录") && div_row_s[j].className === "ant-row")
                    {
                        let div_row_row_s = div_row_s[j].getElementsByTagName("div");
                        for (let k = 0; k < div_row_row_s.length; k++)
                        {
                            if (div_row_row_s[k].innerText.includes('康复指导') && div_row_row_s[k].className === "ant-row")
                            {
                                let fk_label_s = div_row_row_s[k].getElementsByTagName("label");
                                for (let z = 0; z < fk_label_s.length; z++)
                                {
                                    if ((fk_label_s[z].innerText === "穿衣训练，教会穿脱衣裤、鞋袜的方法" || fk_label_s[z].innerText === "教会选择食物及进食的方法"
                                        || fk_label_s[z].innerText === "指导床上运动的目的、方法及注意事项" || fk_label_s[z].innerText === "安全防护指导")
                                        && !fk_label_s[z].className.includes("checked"))
                                        fk_label_s[z].click();

                                }


                            }

                        }
                    }

                }

            }

        }
    }
    //===2222====医养结合======End========




    // =======转诊单======Start=========
    function zhuanZhen()
    {

        // 转诊表 所需变量 start
        const zhuanZhen_hospital = "射洪市人民医院";
        const section = "内科";
        const zhuanZhen_doctor = "王平";

        // 初步印象
        const zhuanZhen_textarea_0 = "没明显症状。";
        // 转出原因
        const zhuanZhen_textarea_1 = "血压控制不稳定。";
        // 既往史
        const zhuanZhen_textarea_2 = "患者多年高血压病史。";
        // 治疗经过
        const zhuanZhen_textarea_3 = "经过治疗，血压控制依然不稳定。";
        // 转诊表 所需变量 End



        let form_s = $('form');
        for (let i=0; i<form_s.length; i++)
        {
            // 找到了目标form表单
            if (form_s[i].innerText.includes('双向转诊单') && form_s[i].innerText.includes('双向转诊(转出)单'))
            {
                let inputs = form_s[i].getElementsByTagName("input");
                inputs[9].value = zhuanZhen_hospital;
                inputs[9].dispatchEvent(fkVueEvent);
                // inputs[16].value = zhuanZhen_hospital;
                // inputs[16].dispatchEvent(fkVueEvent);
                inputs[10].value = section;
                inputs[10].dispatchEvent(fkVueEvent);
                inputs[11].value = zhuanZhen_doctor;
                inputs[11].dispatchEvent(fkVueEvent);
                inputs[12].value = $.cookie("tiJianDate");
                inputs[12].dispatchEvent(fkVueEvent);
                inputs[20].value = $.cookie("tiJianDate");
                inputs[20].dispatchEvent(fkVueEvent);
                inputs[21].value = $.cookie("DoctorTel");
                inputs[21].dispatchEvent(fkVueEvent);

                // 4行备注
                let textarea_s = form_s[i].getElementsByTagName("textarea");
                textarea_s[0].value = zhuanZhen_textarea_0;
                textarea_s[0].dispatchEvent(fkVueEvent);
                textarea_s[1].value = zhuanZhen_textarea_1;
                textarea_s[1].dispatchEvent(fkVueEvent);
                textarea_s[2].value = zhuanZhen_textarea_2;
                textarea_s[2].dispatchEvent(fkVueEvent);
                textarea_s[3].value = zhuanZhen_textarea_3;
                textarea_s[3].dispatchEvent(fkVueEvent);
            }
        }
    }
    // =======转诊单======End=========



    // 程序入口
    document.addEventListener("keydown", function (fuckEvent)
    {
        if (fuckEvent.key === "F9")
        {
            let DllButton = "<div id='fuck.this.shit' " +
                "style='display: block; line-height: 22px; text-align: center; vertical-align: top; background-color: #25ae84; " +
                "cursor: pointer; color: #fff; margin-bottom: 2px; position: fixed; left: 0; top: 358px; width: 102px; z-index: 9999;'>" +
                "<input id = 'tiJianDate' value='" + $.cookie("tiJianDate") + "' style='width: 90px; height: 22px; text-align:center; color: brown;'>" +
                "<input id = 'tiJianDoctor' value='" + $.cookie("tiJianDoctor") + "' style='width: 90px; height: 22px; text-align:center; color: brown;'>" +
                "<input id = 'DoctorTel' value='" + $.cookie("DoctorTel") + "' style='width: 90px; height: 22px; text-align:center; color: brown;'>" +
                "<a id='tiJian_a' target='_blank' style='font-size:13px; color:#fff; display: block; height: 100%; padding: 2px 11px;'>填充体检表</a>" +
                "<a id='yyjh_a' target='_blank' style='font-size:13px; color:#fff; display: block; height: 100%; padding: 2px 11px;'>一键医养结合</a>" +
                "<a id='zhuanzhen_a' target='_blank' style='font-size:13px; color:#fff; display: block; height: 100%; padding: 2px 11px;'>塞满转诊表</a>" +
                "</div>";

            $("body").append(DllButton);
            $("#tiJian_a").click(function ()
            {
                tiJian();
            });
            $("#yyjh_a").click(function ()
            {
                yyjh();
            });
            $("#zhuanzhen_a").click(function()
            {
                zhuanZhen();
            });

            $("#tiJianDate")[0].addEventListener("focusout", function ()
            {
                $.cookie('tiJianDate', $("#tiJianDate")[0].value, { expires: 365, path: '/' });
            });
            $("#tiJianDoctor")[0].addEventListener("focusout", function ()
            {
                $.cookie('tiJianDoctor', $("#tiJianDoctor")[0].value, { expires: 365, path: '/' });
            });
            $("#DoctorTel")[0].addEventListener("focusout", function ()
            {
                $.cookie('DoctorTel', $("#DoctorTel")[0].value, { expires: 365, path: '/' });
            });



        }
    });








})();