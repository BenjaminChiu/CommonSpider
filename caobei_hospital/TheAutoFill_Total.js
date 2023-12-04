// ==UserScript==
// @name         云平台自动化脚本
// @namespace    http://tampermonkey.net/
// @version      0.2.2.0
// @description  适用于健康云平台各类表单的数据填充
// @author       Benjamin Chiu.topfisherman@126.com
// @license MIT
// @icon         https://ehr.scwjxx.cn/favicon.ico
// @match        *://*.scwjxx.cn/*
// @match        *://*.baidu.com/*
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
    const fkVueEvent_blur = new Event("blur", {view: window, bubbles: true, cancelable: false});
    const fkVueEvent_change = new Event("change", {view: window, bubbles: true, cancelable: false});
    // js原生鼠标点击
    // const click_Event = new MouseEvent('click', {'view': window, 'bubbles': true, 'cancelable': true});



    // 字典 村医的联系方式
    const cun_doctor_tel = {"王祥茂":"13547784526", "胥德顺":"13882507277", "王晏":"15108117003", "覃蒲昌":"15082588136",
        "蒲兴周":"15181944660", "付建兴":"13882549411", "任朝龙":"15182548314", "胥学领":"15388349328", "蒲泽华":"15983086284",
        "王平":"18980189346", "廖先志":"19827454586", "杨荣":"15328520078", "赵中全":"15108117301", "王军":"18280866037"};



    // =======Util-1====封装人体常见体征数据==========
    function bodyDATA()
    {

        // 人体常见体征数据
        // 体温   为什么是string？
        const body_temperature = (Math.random() * (36.9 - 36) + 36).toFixed(1);
        // 脉搏
        const pulse_rate = Math.floor(Math.random() * (82 - 68 + 1)) + 68;
        // 呼吸频率
        const respiratory_rate = Math.floor(Math.random() * (20 - 16 + 1)) + 16;
        // 高压
        const blood_pressure_high = Math.floor(Math.random() * (132 - 118 + 1)) + 118;
        // 低压
        const blood_pressure_low = Math.floor(Math.random() * (86 - 74 + 1)) + 74;
        // 高压
        const blood_pressure_high_2 = Math.floor(Math.random() * (132 - 118 + 1)) + 118;
        // 低压
        const blood_pressure_low_2 = Math.floor(Math.random() * (86 - 74 + 1)) + 74;

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

         // 封装数据并返回
         const bodyDATA = new Map();
         bodyDATA.set("body_temperature", body_temperature);
         bodyDATA.set("pulse_rate", pulse_rate);
         bodyDATA.set("respiratory_rate", respiratory_rate);
         bodyDATA.set("blood_pressure_high", blood_pressure_high);
         bodyDATA.set("blood_pressure_low", blood_pressure_low);
         bodyDATA.set("blood_pressure_high_2", blood_pressure_high_2);
         bodyDATA.set("blood_pressure_low_2", blood_pressure_low_2);

         bodyDATA.set("hemoglobin", hemoglobin);
         bodyDATA.set("hemameba", hemameba);
         bodyDATA.set("blood_platelet", blood_platelet);
         bodyDATA.set("blood_sugar", blood_sugar);
         bodyDATA.set("blood_sugar_high", blood_sugar_high);


        return bodyDATA;
    }



    // =======Util-2====获取是高血压还是糖尿病随访==========
    function get_sickness_status()
    {
        // 为什么将高血压/糖尿病status放在全局变量位置，因为转诊函数和随访结局函数都会用到
        // 高血压为True；糖尿病为False
        let sickness_status = true;

        let sickness_div_s = $('div.header-left.right-header:first');
        for(let i=0; i<sickness_div_s.length; i++)
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



    // ========Util-3====获取当前村医生===来自左上角签约信息==========
    function get_cun_doctor()
    {
        // 全局变量，容纳当前村医生
        let cun_doctor = $.cookie("tiJianDoctor");

        let button_s = $('button');
        for (let i= 0; i< button_s.length; i++)
        {
            if (button_s[i].innerText.includes('健康档案'))
                cun_doctor = button_s[i].childNodes[3].innerText
        }

        return cun_doctor;
    }




    // ===功能模块-1====体检表======Start=========
    function tiJian()
    {
        console.log("正在使用体检表填充功能.");

        // 修改体检表标签
        let edit_flag = false;



        // ====Start======第4页监听器=================
        // 解决点击第4页时，自动取消“4锻炼”按钮
        const div_s  = document.getElementsByTagName("div");
        for (let i=0; i<div_s.length; i++)
        {
            if (div_s[i].innerText === "第4页")
            {
                div_s[i].addEventListener("mousedown", function (fuckEvent)
                {
                    for (let j=0; j<div_s.length; j++)
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



        // 自动识别模块
        // 1. 获取姓名
        let OldManName = '';
        let name_div_s = $('div.ant-col');
        for (let i=0; i<name_div_s.length; i++)
        {
            if (name_div_s[i].innerText.includes('姓名'))
            {
                OldManName= name_div_s[i].getElementsByTagName("span")[0].innerText;
                // 一个值就够，终结循环
                if (OldManName !== '' && OldManName !== '姓名' && OldManName !== undefined)
                    break;
            }
        }
        console.log("当前病人：" + OldManName);






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

                        let div_s = tr_s[j].getElementsByTagName("div");
                        for (let k=0; k<div_s.length; k++)
                        {
                            if (div_s[k].hasAttribute('title'))
                            {
                                div_s[k].setAttribute('title', '王芳 (射洪市曹碑镇卫生院)');
                                div_s[k].dispatchEvent(fkVueEvent_change);
                                inputs[1].value = '王芳 (射洪市曹碑镇卫生院)';
                                inputs[1].dispatchEvent(fkVueEvent_change);
                            }

                        }
                    }
                    else if (tr_s[j].innerText.includes("体温") && tr_s[j].innerText.includes("脉率"))
                    {
                        let inputs = tr_s[j].getElementsByTagName("input");
                        inputs[0].value = body_temperature;
                        inputs[0].dispatchEvent(fkVueEvent);
                        inputs[1].value = pulse_rate.toString();
                        inputs[1].dispatchEvent(fkVueEvent);
                    }
                    else if (tr_s[j].innerText.includes("呼吸频率") && tr_s[j].innerText.includes("左侧"))
                    {
                        let inputs = tr_s[j].getElementsByTagName("input");
                        inputs[0].value = respiratory_rate.toString();
                        inputs[0].dispatchEvent(fkVueEvent);
                        inputs[1].value = blood_pressure_high.toString();
                        inputs[1].dispatchEvent(fkVueEvent);
                        inputs[2].value = blood_pressure_low.toString();
                        inputs[2].dispatchEvent(fkVueEvent);
                    }
                    else if (tr_s[j].innerText.includes("右侧") && !tr_s[j].innerText.includes("右侧弱"))
                    {
                        let inputs = tr_s[j].getElementsByTagName("input");
                        inputs[0].value = blood_pressure_high_2.toString();
                        inputs[0].dispatchEvent(fkVueEvent);
                        inputs[1].value = blood_pressure_low_2.toString();
                        inputs[1].dispatchEvent(fkVueEvent);
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

                        setTimeout(function ()
                        {
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
                                    button_s[1].click();
                                }
                            }
                        }, 600);
                    }


                    else if (tr_s[j].innerText.includes("尿蛋白"))
                    {
                        let input_s = tr_s[j].getElementsByTagName("input");
                        // 尿蛋白
                        input_s[0].value = "-";
                        input_s[0].dispatchEvent(fkVueEvent);
                        input_s[0].dispatchEvent(fkVueEvent_blur);
                        // 尿糖
                        input_s[1].value = "+++";
                        input_s[1].dispatchEvent(fkVueEvent);
                        input_s[1].dispatchEvent(fkVueEvent_blur);
                    }
                    else if(tr_s[j].innerText.includes("尿酮体"))
                    {
                        let input_s = tr_s[j].getElementsByTagName("input");
                        // 尿酮体
                        input_s[0].value = "+-";
                        input_s[0].dispatchEvent(fkVueEvent);
                        input_s[0].dispatchEvent(fkVueEvent_blur);
                        // 尿潜血
                        input_s[1].value = "+-";
                        input_s[1].dispatchEvent(fkVueEvent);
                        input_s[1].dispatchEvent(fkVueEvent_blur);
                    }

                    else if (tr_s[j].innerText.includes("心电图"))
                    {
                        const divs = tr_s[j].getElementsByTagName("div");
                        for (let i = 0; i < divs.length; i++)
                        {
                            if (divs[i].innerText.includes('1正常') && !divs[i].className.includes('checked'))
                                divs[i].click();
                        }
                        // let textarea_s = tr_s[j].getElementsByTagName("textarea");
                        // textarea_s[0].value = "轻微心电左偏";
                        // textarea_s[0].dispatchEvent(fkVueEvent);
                    }
                    else if (tr_s[j].innerText.includes("腹部B超"))
                    {
                        const divs = tr_s[j].getElementsByTagName("div");
                        for (let i = 0; i < divs.length; i++)
                        {
                            if (divs[i].innerText.includes('1正常') && !divs[i].className.includes('checked'))
                                divs[i].click();
                        }
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
                        textarea_s[0].value = "预防骨质疏松、预防跌倒";
                        textarea_s[0].dispatchEvent(fkVueEvent);

                        textarea_s[1].value = "流感疫苗、肺炎疫苗";
                        textarea_s[1].dispatchEvent(fkVueEvent);
                    }
                }
            }
        }
    }
    // ===1111====体检表======End=========





    // ===功能模块-2====转诊单======Start=========
    function zhuanZhen()
    {
        console.log("测试使用，已进入转诊函数");

        // 获取是高血压还是糖尿病
        let sickness_flag = get_sickness_status();


        // 转诊表 所需变量 start
        let zhuanZhen_hospital = "射洪市人民医院";
        let section = "内科";
        let zhuanZhen_doctor = "王老师";
        // 初步印象
        let zhuanZhen_textarea_0 = "患者无明显自觉症状。";
        // 转出原因
        let zhuanZhen_textarea_1 = "血压控制不满意。";
        // 既往史
        let zhuanZhen_textarea_2 = "患者有高血压病史。";
        // 治疗经过
        let zhuanZhen_textarea_3 = "经过治疗，血压控制依然不满意。";


        if (!sickness_flag)
        {
            zhuanZhen_hospital = "射洪市人民医院";
            section = "内分泌科";
            zhuanZhen_doctor = "赵老师";

            zhuanZhen_textarea_1 = "空腹血糖控制不满意";
            zhuanZhen_textarea_2 = "患者有糖尿病病史。";
            zhuanZhen_textarea_3 = "经过治疗，空腹血糖控制依然不满意。";
        }


        // 转诊表 所需变量 End



        // 转诊的村医姓名
        let cun_doctor = get_cun_doctor();




        // 填充数据
        let form_s = $('form');
        for (let i=0; i<form_s.length; i++)
        {
            // 找到了目标form表单
            if (form_s[i].innerText.includes('双向转诊单') && form_s[i].innerText.includes('双向转诊(转出)单'))
            {
                let inputs = form_s[i].getElementsByTagName("input");
                inputs[9].value = zhuanZhen_hospital;
                inputs[9].dispatchEvent(fkVueEvent);
                inputs[16].value = zhuanZhen_hospital;
                inputs[16].dispatchEvent(fkVueEvent);
                inputs[10].value = section;
                inputs[10].dispatchEvent(fkVueEvent);

                inputs[11].value = zhuanZhen_doctor;
                inputs[11].dispatchEvent(fkVueEvent);

                // 自动捕获村医
                inputs[12].value = cun_doctor;
                inputs[12].dispatchEvent(fkVueEvent);

                inputs[20].value = cun_doctor;
                inputs[20].dispatchEvent(fkVueEvent);

                inputs[21].value = cun_doctor_tel[cun_doctor];  // 用村医姓名查找村医的电话号码
                console.log("fucking Test.Tel="+inputs[21].value+";Doc="+inputs[20].value);
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

                break;
            }
        }


        console.log("测试使用，已结束执行转诊函数");

    }
    // =======转诊单======End=========





    // ===功能模块-3===随访结局=====Start==========
    function suiFangResult()
    {
        console.log("随访结局测试使用，已进入随访结局函数");
        // 获取是高血压还是糖尿病
        let sickness_flag = get_sickness_status();

        // 给定一个确认弹窗
        // let the_Result = confirm("随访结局是否满意？\n'确认'代表满意！'取消'代表不满意！");
        let the_Result = true;


        // 如果先找到了随访结局，没有找到随访分类的flag，怎么办？

        // 设定一个修改flag
        let result_flag = false;
        let cun_doctor_flag = false;

        let tr_s = $('tr');     // 找table中的一行tr
        for (let i=0; i<tr_s.length; i++)
        {

            if (tr_s[i].innerText.includes('此次随访分类'))
            {
                let div_s = tr_s[i].getElementsByTagName("div");
                for (let j=0; j<div_s.length; j++)
                {
                    if(div_s[j].innerText.includes("1控制满意") && div_s[j].className.includes('checked'))
                        the_Result = true;
                    else if (div_s[j].innerText.includes("2控制不满意") && div_s[j].className.includes('checked'))
                        the_Result = false;
                }

            }

                // else if (tr_s[i].innerText.includes('随访方式'))
                // {
                //     let div_s = tr_s[i].getElementsByTagName("div");
                //     for (let j=0; j < div_s.length; j++)
                //     {
                //         if (div_s[j].innerText.includes("2家庭") && div_s[j].className.includes("ant-tag-checkable")
                //             && !div_s[j].className.includes("checked"))
                //             div_s[j].click();
                //     }
            // }

            else if (tr_s[i].innerText.includes('随访结局'))
            {
                let textarea_s = tr_s[i].getElementsByTagName("textarea");
                if (sickness_flag)
                    textarea_s[0].value = the_Result ? '已随访，血压控制满意。' : '已随访，血压控制不满意。';
                else
                    textarea_s[0].value = the_Result ? '已随访，空腹血糖控制满意。' : '已随访，空腹血糖控制不满意。';

                if (!result_flag)
                {
                    textarea_s[0].dispatchEvent(fkVueEvent);
                    result_flag = true;     // 修改完成后，重置修改标志
                }

            }

            else if (tr_s[i].innerText.includes('随访医生'))
            {
                // 步骤一：模拟点击下拉框，触发事件，获取下拉数据；如不点击获取不到相应下拉数据
                let div_s = tr_s[i].getElementsByTagName("div");
                for (let j=0; j<div_s.length; j++)
                {
                    if ("combobox" === div_s[j].getAttribute("role"))
                    {
                        // div_s[j].dispatchEvent(click_Event);     原生JS报错new ClickEvent构建错误
                        div_s[j].click();

                        break;  // 目的达到，结束循环
                    }
                }


                // 步骤二：模拟点击选取对应村医生
                setTimeout(function ()
                {
                    let ul_s = $('ul[role="listbox"]');
                    for (let j=0; j<ul_s.length; j++)
                    {
                        if (ul_s[j].innerText.includes('曹碑镇卫生院'))
                        {
                            let li_s = ul_s[j].getElementsByTagName("li");
                            for (let z=0; z<li_s.length; z++)
                            {
                                if (li_s[z].innerText.includes(get_cun_doctor()) && !cun_doctor_flag)
                                {
                                    li_s[z].click();
                                    cun_doctor_flag = true;
                                }

                            }
                        }
                    }
                }, 500);
            }



        }








        console.log("随访结局测试使用，已退出随访结局函数");
    }

    // ======随访结局=====End==========






    // 程序入口
    document.addEventListener("keydown", function (fuckEvent)
    {
        if (fuckEvent.key === "F9")
        {
            console.log("您已按下F9，实现弹窗，StartFunction");


            $("body").append('<style>' +
                '.switch_xxx {position: relative;display: inline-block;width: 30px;height: 17px;}' +
                '.switch_xxx input {opacity: 0;width: 0;height: 0;}' +
                '.slider_xxx {position: absolute;cursor: pointer;top: 0;left: 0;right: 0;bottom: 0;background-color: #ccc;transition: .4s;}' +
                '.slider_xxx:before {position: absolute;content: "";height: 13px;width: 13px;left: 2px;bottom: 2px;background-color: white;transition: .4s;}' +
                '#togBtn:checked + .slider_xxx {background-color: green;}' +
                '#togBtn:focus + .slider_xxx {box-shadow: 0 0 1px green;}' +
                '#togBtn:checked + .slider_xxx:before {transform: translateX(13px);}' +
                '.slider_xxx.round_xxx {border-radius: 17px;}' +
                '.slider_xxx.round_xxx:before {border-radius: 50%;}' +
                '</style>');




            let DllButton = "<div id='fuck.this.shit' style='font-family: SimSun,fangsong; font-weight: bold; display: block; line-height: 22px; " +
                "text-align: center; vertical-align: center; background-color: #25ae84; cursor: pointer; margin: 2px; position: fixed; left: 0; top: 185px; width: 80px; z-index: 8888;'>" +

                // "<a id='tiJian_a' target='_blank' style='font-size:13px; color:#fff; display: block; height: 100%; padding: 2px 11px;'>填充体检表</a>" +
                // "<input id = 'tiJianDate' placeholder='体检日期' value='" + $.cookie("tiJianDate") + "' style='width: 90px; height: 22px; text-align:center; color: brown;'>" +

                // "<input id = 'tiJianDoctor' placeholder='村医生名字' value='" + $.cookie("tiJianDoctor") + "' style='width: 90px; height: 22px; text-align:center; color: brown;'>" +
                // "<input id = 'DoctorTel' placeholder='村医生电话' value='" + $.cookie("DoctorTel") + "' style='width: 90px; height: 22px; text-align:center; color: brown;'>" +

                "<a id='zhuanzhen_a' target='_blank' style='font-size:15px; color:#fff; display: block; height: 100%; padding: 3px 1px;'" +
                " onmouseover=\"this.style.color='red'\" onmouseout=\"this.style.color='white'\">转诊表</a>" +
                "<div style='height: 4px;'></div>"+

                "<label style='font-size:10px; color:aquamarine; display: block; height: 100%; padding: 3px 1px;'>" +
                "<label class=\"switch_xxx\"><input type=\"checkbox\" id=\"togBtn\"><div class=\"slider_xxx round_xxx\"></div></label>血压心率</label>" +

                "<a id='suiFangResult_a' target='_blank' style='font-size:15px; color:#fff; display: block; height: 100%; padding: 3px 1px;'" +
                " onmouseover=\"this.style.color='red'\" onmouseout=\"this.style.color='white'\">完善随访</a>" +


                "</div>";

            $("body").append(DllButton);

            // $("#tiJian_a").click(function ()
            // {
            //     tiJian();
            // });

            // $("#tiJianDate")[0].addEventListener("focusout", function ()
            // {
            //     $.cookie('tiJianDate', $("#tiJianDate")[0].value, { expires: 365, path: '/' });
            // });


            $("#zhuanzhen_a").click(function()
            {
                zhuanZhen();
            });


            $("#suiFangResult_a").click(function()
            {
                suiFangResult();
            });


            console.log("您已按下F9，实现弹窗，EndFunction");

        }
    });





})();