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

    // Function on/off
    const tiJianDATE_Flag = true;      // 日期填充（体检、随访）
    const tiJian_Dll_Flag = true;       // 体检表填充
    const suiFang_Dll_Flag = true;      // 随访模块

    // 局部功能开关（随访）
    const sf_day = true;               // 随访日期
    const sf_way = true;               // 随访方式
    const sf_blood_pressure = false;    // 随访血压
    const next_sf_day = false;          // 下一次随访日期
    const next_sf_day_value = "2024-08-30";    // 下一次随访日期值

    const special_next_sf_day_value = "2024-05-30";    // 下一次随访日期值


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
    const cun_doctor_tel = {
        "王祥茂": "13547784526",
        "胥德顺": "13882507277",
        "王晏": "15108117003",
        "覃蒲昌": "15082588136",
        "蒲兴周": "15181944660",
        "付建兴": "13882549411",
        "任朝龙": "15182548314",
        "胥学领": "15388349328",
        "蒲泽华": "15983086284",
        "王平": "18980189346",
        "廖先志": "19827454586",
        "杨荣": "15328520078",
        "赵中全": "15108117301",
        "王军": "18280866037"
    };


    const g_s_1 = "1.减钠增钾，饮食清淡。2.合理膳食，科学食养。3.吃动平衡，健康体重，心理平衡。4.监测血压，自我管理。";
    const g_s_2 = "合理膳食，饮食清淡，吃动平衡，健康体重。监测血压，自我管理。";
    const g_s = [g_s_1, g_s_2];

    const t_s_1 = "1.食物多样，养成和建立合理膳食习惯。2.能量适宜，控制超重肥胖和预防消瘦。3.主食定量，优选全谷物和低血糖生成指数食物。4.积极运动，改善体质和胰岛素敏感性。" +
        "5.清淡饮食，预防和延缓并发症。6.食养有道，合理选择应用食药物质。7.规律进餐，合理加餐，促进餐后血糖稳定。8.自我管理，定期营养咨询，提高血糖控制能力。";
    const t_s_2 = "饮食多样，合理膳食。主食定量，积极运动。清淡饮食，规律进餐。";
    const t_s = [t_s_1, t_s_2];

    const u_s_1 = "食物多样、搭配合理，符合平衡膳食要求。能量供给与机体需要相适应，吃动平衡，维持健康体重。保证优质蛋白质、矿物质、维生素的供给。" +
        "烹制食物适合咀嚼、吞咽和消化。饮食清淡，注意食品卫生。食物摄入无法满足需要时，合理进行营养素补充。";
    const u_s_2 = "食物多样、搭配合理。吃动平衡，健康体重。保证优质蛋白质、矿物质、维生素的供给";
    const u_s = [u_s_1, u_s_2];

    const the_final = "清淡饮食，畅情志。";


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
            'respiratory_rate': Math.floor(Math.random() * (20 - 16 + 1)) + 16
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
                        // 体检日期
                        if (tiJianDATE_Flag)
                        {
                            let inputs = tr_s[j].getElementsByTagName("input");
                            inputs[0].value = $.cookie("tiJianDate");
                            inputs[0].dispatchEvent(fkVueEvent_change);
                        }

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
                        }, 500);

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
                        if (sickness_flag["gxy"])
                        {
                            inputs[1].value = body_DATA_gao['blood_pressure_high'].toString();
                            inputs[2].value = body_DATA_gao['blood_pressure_low'].toString();
                        }
                        else
                        {
                            inputs[1].value = body_DATA['blood_pressure_high'].toString();
                            inputs[2].value = body_DATA['blood_pressure_low'].toString();
                        }
                        inputs[1].dispatchEvent(fkVueEvent);
                        inputs[2].dispatchEvent(fkVueEvent);
                    }
                    else if (tr_s[j].innerText.includes("右侧") && !tr_s[j].innerText.includes("右侧弱"))
                    {
                        let inputs = tr_s[j].getElementsByTagName("input");
                        if (sickness_flag["gxy"])
                        {
                            inputs[0].value = body_DATA_gao['blood_pressure_high_2'].toString();
                            inputs[1].value = body_DATA_gao['blood_pressure_low_2'].toString();
                        }
                        else
                        {
                            inputs[0].value = body_DATA['blood_pressure_high_2'].toString();
                            inputs[1].value = body_DATA['blood_pressure_low_2'].toString();
                        }
                        inputs[0].dispatchEvent(fkVueEvent);
                        inputs[1].dispatchEvent(fkVueEvent);
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


                        // else if (tr_s[j].innerText.includes("足背脉搏动") && sickness_flag["tyb"])
                        // {
                        //     const divs = tr_s[j].getElementsByTagName("div");
                        //     for (let k = 0; k < divs.length; k++)
                        //     {
                        //         if (divs[k].innerText.includes("2触及双侧对称") && !divs[k].className.includes('checked'))
                        //         {
                        //             divs[k].click();
                        //         }
                        //     }
                        // }


                        // else if (tr_s[j].innerText.includes("尿蛋白") && tr_s[j].innerText.includes("尿糖"))
                        // {
                        //     let input_s = tr_s[j].getElementsByTagName("input");
                        //     // 尿蛋白
                        //     input_s[0].value = "-";
                        //     input_s[0].dispatchEvent(fkVueEvent);
                        //     input_s[0].dispatchEvent(fkVueEvent_blur);
                        //     // 尿糖
                        //     input_s[1].value = "-";
                        //     input_s[1].dispatchEvent(fkVueEvent);
                        //     input_s[1].dispatchEvent(fkVueEvent_blur);
                        // }
                        // else if (tr_s[j].innerText.includes("尿酮体") && tr_s[j].innerText.includes("尿潜血"))
                        // {
                        //     let input_s = tr_s[j].getElementsByTagName("input");
                        //     // 尿酮体
                        //     input_s[0].value = "-";
                        //     input_s[0].dispatchEvent(fkVueEvent);
                        //     input_s[0].dispatchEvent(fkVueEvent_blur);
                        //     // 尿潜血
                        //     input_s[1].value = "-";
                        //     input_s[1].dispatchEvent(fkVueEvent);
                        //     input_s[1].dispatchEvent(fkVueEvent_blur);
                        // }

                        // else if (tr_s[j].innerText.includes("心电图"))
                        // {
                        //     const divs = tr_s[j].getElementsByTagName("div");
                        //     for (let k = 0; k < divs.length; k++)
                        //     {
                        //         if (divs[k].innerText.includes('1正常') && !divs[k].className.includes('checked'))
                        //         {
                        //             divs[k].click();
                        //         }
                        //     }
                        // }

                        // else if (tr_s[j].innerText.includes("腹部B超"))
                        // {
                        //     const divs = tr_s[j].getElementsByTagName("div");
                        //     for (let k = 0; k < divs.length; k++)
                        //     {
                        //         if (divs[k].innerText.includes('1正常') && !divs[k].className.includes('checked'))
                        //         {
                        //             divs[k].click();
                        //         }
                        //     }
                        // }

                        // else if (tr_s[j].innerText.includes("其他系统疾病") && (sickness_flag["gxy"] || sickness_flag["tyb"]))
                        // {
                        //     console.log("慢病备注Debug");
                        //     let edit_flag = false;
                        //
                        //     const divs = tr_s[j].getElementsByTagName("div");
                        //     for (let k = 0; k < divs.length; k++)
                        //     {
                        //         if (divs[k].innerText.includes("2有异常") && !divs[k].className.includes('checked'))
                        //         {
                        //             divs[k].click();
                        //             edit_flag = true;
                        //         }
                        //     }
                        //
                        //     if (!edit_flag)
                        //     {
                        //         setTimeout(function ()
                        //         {
                        //             let textarea_s = tr_s[j].getElementsByTagName("textarea");
                        //             if (sickness_flag["gxy"] && !textarea_s[0].innerText.includes("原发性高血压"))
                        //                 textarea_s[0].value = textarea_s[0].value + "原发性高血压 ";
                        //             if (sickness_flag["tyb"] && !textarea_s[0].innerText.includes("二型糖尿病"))
                        //                 textarea_s[0].value = textarea_s[0].value + "二型糖尿病";
                        //             textarea_s[0].dispatchEvent(fkVueEvent);
                        //         }, 400);
                        //     }
                        // }


                        // else if (tr_s[j].innerText.includes("危险因素控制"))
                        // {
                        //     const divs = tr_s[j].getElementsByTagName("div");
                        //     for (let k = 0; k < divs.length; k++)
                        //     {
                        //         if ((divs[k].innerText.includes('3') || divs[k].innerText.includes('4')
                        //                 || divs[k].innerText.includes('6') || divs[k].innerText.includes('7'))
                        //             && !divs[k].className.includes('checked'))
                        //         {
                        //             divs[k].click();
                        //         }
                        //     }
                        //     let textarea_s = tr_s[j].getElementsByTagName("textarea");
                        //     textarea_s[0].value = "预防骨质疏松、预防跌倒";
                        //     textarea_s[0].dispatchEvent(fkVueEvent);
                        //
                        //     textarea_s[1].value = "流感疫苗、肺炎疫苗";
                        //     textarea_s[1].dispatchEvent(fkVueEvent);
                    // }

                    else if (tr_s[j].innerText.includes("健康摘要"))
                    {
                        let textarea_s = tr_s[j].getElementsByTagName("textarea");

                        // if (sickness_flag["gxy"] && !sickness_flag["tyb"])
                        //     textarea_s[0].value = g_s[Math.floor(Math.random() * g_s.length)];
                        // else if (!sickness_flag["gxy"] && sickness_flag["tyb"])
                        //     textarea_s[0].value = t_s[Math.floor(Math.random() * t_s.length)];
                        // else if (sickness_flag["gxy"] && sickness_flag["tyb"])
                        //     textarea_s[0].value = t_s[Math.floor(Math.random() * t_s.length)];
                        // else
                        //     textarea_s[0].value = u_s[Math.floor(Math.random() * u_s.length)];

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


    // =========Function-2====转诊单==============
    function zhuanZhen()
    {
        console.log("测试使用，已进入转诊函数");

        // 外部获取 是高血压还是糖尿病
        let sickness_flag = get_sickness_status();
        // 外部获取 转诊的村医姓名
        let cun_doctor = get_cun_doctor();


        // 步骤一：生成数据     转诊表 所需变量 start
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


        // 步骤二：填充数据
        let form_s = $('form');
        for (let i = 0; i < form_s.length; i++)
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
                console.log("fucking Test.Tel=" + inputs[21].value + ";Doc=" + inputs[20].value);
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


    // =========Function-3====随访结局=============
    function suiFangResult()
    {
        console.log("随访结局测试使用，已进入随访结局函数");

        // 获取是高血压还是糖尿病
        let sickness_flag = get_sickness_status();
        // 外部获取 转诊的村医姓名
        let cun_doctor = get_cun_doctor();
        // 外部获取体征数据
        let body_DATA = get_body_DATA(sickness_flag);


        // 设定一个修改flag
        let result_flag = false;
        let cun_doctor_flag = false;
        // flag 随访结局是否满意
        let the_Result = true;


        let tr_s = $('tr');     // 找table中的一行tr
        for (let i = 0; i < tr_s.length; i++)
        {
            if ((tr_s[i].innerText.includes('随访日期') || tr_s[i].innerText.includes('随访方式'))
                && !tr_s[i].innerText.includes('下次随访日期'))
            {
                // 随访日期
                if (sf_day && tiJianDATE_Flag)
                {
                    let inputs = tr_s[i].getElementsByTagName("input");
                    inputs[0].value = $.cookie("tiJianDate");
                    inputs[0].dispatchEvent(fkVueEvent_change);
                }
                if (sf_way)
                {
                    let div_s = tr_s[i].getElementsByTagName("div");
                    for (let j = 0; j < div_s.length; j++)
                    {
                        if (div_s[j].innerText.includes("2家庭") && div_s[j].className.includes("ant-tag-checkable")
                            && !div_s[j].className.includes("checked"))
                            div_s[j].click();
                    }
                }
            }

            else if (!(tr_s[i].innerText.includes('随访日期') || tr_s[i].innerText.includes('随访方式'))
                && tr_s[i].innerText.includes('下次随访日期'))
            {
                // 下一次随访日期
                if (next_sf_day)
                {
                    let inputs = tr_s[i].getElementsByTagName("input");
                    inputs[0].value = next_sf_day_value;
                    inputs[0].dispatchEvent(fkVueEvent_change);
                }
            }

            else if (tr_s[i].innerText.includes('血压') && sf_blood_pressure)
            {
                let input_s = tr_s[i].getElementsByTagName("input");
                input_s[0].value = body_DATA['blood_pressure_high'];
                input_s[1].value = body_DATA['blood_pressure_low'];

                input_s[0].dispatchEvent(fkVueEvent);
                input_s[1].dispatchEvent(fkVueEvent);
            }


            else if (tr_s[i].innerText.includes('此次随访分类'))
            {
                let div_s = tr_s[i].getElementsByTagName("div");
                for (let j = 0; j < div_s.length; j++)
                {
                    if (div_s[j].innerText.includes("1控制满意") && div_s[j].className.includes('checked'))
                        the_Result = true;
                    else if (div_s[j].innerText.includes("2控制不满意") && div_s[j].className.includes('checked'))
                        the_Result = false;
                }
            }

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

            else if (tr_s[i].innerText.includes('健康指导'))
            {
                let textarea_s = tr_s[i].getElementsByTagName("textarea");

                // if (sickness_flag)
                //     textarea_s[0].value = g_s[Math.floor(Math.random() * g_s.length)];
                // else
                //     textarea_s[0].value = t_s[Math.floor(Math.random() * t_s.length)];

                textarea_s[0].value = the_final;
                textarea_s[0].dispatchEvent(fkVueEvent);
            }

            else if (tr_s[i].innerText.includes('随访医生'))
            {
                console.log("进入随访医生模块");
                // 步骤一：模拟点击下拉框，触发事件，获取下拉数据；如不点击获取不到相应下拉数据
                let div_s = tr_s[i].getElementsByTagName("div");
                for (let j = 0; j < div_s.length; j++)
                {
                    if ("combobox" === div_s[j].getAttribute("role"))
                    {
                        // div_s[j].dispatchEvent(click_Event);     原生JS报错new ClickEvent构建错误
                        div_s[j].click();
                        break;  // 目的达到，结束内循环
                    }
                }


                // 步骤二：模拟点击选取对应村医生
                setTimeout(function ()
                {
                    let ul_s = $('ul[role="listbox"]');
                    for (let j = 0; j < ul_s.length; j++)
                    {
                        if (ul_s[j].innerText.includes('曹碑镇卫生院'))
                        {
                            let li_s = ul_s[j].getElementsByTagName("li");
                            for (let z = 0; z < li_s.length; z++)
                            {
                                // 关键：如果下拉列表中有村医 和 签约的村医一致，则点击该村医
                                if (li_s[z].innerText.includes(cun_doctor) && !cun_doctor_flag
                                    && !li_s[z].innerText.includes("禁") && !li_s[z].innerText.includes("停"))
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

    }


    // =========Function-4====sf-day=============
    function sfDay()
    {
        console.log("已进入-专业修改随访日期函数");


        let tr_s = $('tr');     // 找table中的一行tr
        for (let i = 0; i < tr_s.length; i++)
        {
            if (tr_s[i].innerText.includes('下次随访日期'))
            {
                // 下一次随访日期

                let inputs = tr_s[i].getElementsByTagName("input");
                inputs[0].value = special_next_sf_day_value;
                inputs[0].dispatchEvent(fkVueEvent_change);
            }

        }

    }


    // ===================生成指定范围内的整数=====================
    function randomInt(min, max)
    {
        return Math.floor(Math.random() * (max - min + 1) + min);
    }


    function templateFun(tr_s, i, randNum, selectNum1, selectNum2)
    {
        let divs = tr_s[i].getElementsByTagName("div");

        const the_value_flag = randomInt(0, 9) < randNum;

        if (the_value_flag && !divs[selectNum1].className.includes('checked'))
            divs[selectNum1].click();
        else if (!the_value_flag && !divs[selectNum2].className.includes('checked'))
            divs[selectNum2].click();
    }


    // =========Function-5====中医=============
    function zhongYi()
    {
        console.log("已进入-中医保健函数");


        let tr_s = $('tr');     // 找table中的一行tr
        for (let i = 0; i < tr_s.length; i++)
        {
            if (tr_s[i].innerText.includes('您精力充沛吗'))
                templateFun(tr_s, i, 6, 3, 2)
            else if (tr_s[i].innerText.includes('您容易疲乏吗'))
                templateFun(tr_s, i, 6, 1, 2)
            else if (tr_s[i].innerText.includes('您容易气短'))
                templateFun(tr_s, i, 6, 1, 2)
            else if (tr_s[i].innerText.includes('您说话声音低弱无力吗'))
                templateFun(tr_s, i, 6, 1, 2)
            else if (tr_s[i].innerText.includes('您感到闷闷不乐'))
                templateFun(tr_s, i, 7, 1, 2)
            else if (tr_s[i].innerText.includes('您容易精神紧张'))
                templateFun(tr_s, i, 6, 3, 2)
            else if (tr_s[i].innerText.includes('您因为生活状态改变而感到孤独'))
                templateFun(tr_s, i, 7, 3, 2)
            else if (tr_s[i].innerText.includes('您容易感到害怕或受到惊吓吗'))
                templateFun(tr_s, i, 7, 3, 1)
            else if (tr_s[i].innerText.includes(')您感到身体超重不轻松吗'))
                templateFun(tr_s, i, 6, 2, 1)
            else if (tr_s[i].innerText.includes('您眼睛干涩吗'))
                templateFun(tr_s, i, 6, 3, 2)
            else if (tr_s[i].innerText.includes('您手脚发凉吗'))
                templateFun(tr_s, i, 7, 3, 2)
            else if (tr_s[i].innerText.includes('背部或腰膝部怕冷吗'))
                templateFun(tr_s, i, 6, 2, 1)
            else if (tr_s[i].innerText.includes('您比一般人耐受不了寒冷吗'))
                templateFun(tr_s, i, 6, 2, 1)
            else if (tr_s[i].innerText.includes('您容易患感冒吗'))
                templateFun(tr_s, i, 6, 2, 3)
            else if (tr_s[i].innerText.includes('您没有感冒时也会鼻塞'))
                templateFun(tr_s, i, 6, 0, 2)
            else if (tr_s[i].innerText.includes('您有口粘口腻'))
                templateFun(tr_s, i, 6, 0, 2)
            else if (tr_s[i].innerText.includes('花粉或在季节交替'))
                templateFun(tr_s, i, 8, 0, 1)
            else if (tr_s[i].innerText.includes('您的皮肤容易起荨麻疹吗'))
                templateFun(tr_s, i, 6, 0, 1)
            else if (tr_s[i].innerText.includes('您的皮肤在不知不觉中会出现青紫瘀斑'))
                templateFun(tr_s, i, 6, 0, 1)
            else if (tr_s[i].innerText.includes('指被指甲或钝物划过后皮肤的反应'))
                templateFun(tr_s, i, 6, 0, 2)
            else if (tr_s[i].innerText.includes('您皮肤或口唇干吗'))
                templateFun(tr_s, i, 6, 1, 2)
            else if (tr_s[i].innerText.includes('您有肢体麻木或固定部位疼痛的感觉吗'))
                templateFun(tr_s, i, 6, 1, 2)
            else if (tr_s[i].innerText.includes('您面部或鼻部有油腻感或者油亮发光吗'))
                templateFun(tr_s, i, 7, 1, 0)
            else if (tr_s[i].innerText.includes('您面色或目眶晦黯'))
                templateFun(tr_s, i, 6, 0, 1)
            else if (tr_s[i].innerText.includes('您有皮肤湿疹'))
                templateFun(tr_s, i, 8, 0, 1)
            else if (tr_s[i].innerText.includes('您感到口干咽燥、总想喝水吗'))
                templateFun(tr_s, i, 7, 1, 0)
            else if (tr_s[i].innerText.includes('您感到口苦或嘴里有异味吗'))
                templateFun(tr_s, i, 7, 0, 2)
            else if (tr_s[i].innerText.includes('您腹部肥大吗'))
                templateFun(tr_s, i, 7, 0, 2)
            else if (tr_s[i].innerText.includes('凉的东西会感到不舒服或者怕吃'))
                templateFun(tr_s, i, 5, 2, 3)
            else if (tr_s[i].innerText.includes('您有大便黏滞不爽'))
                templateFun(tr_s, i, 6, 1, 3)
            else if (tr_s[i].innerText.includes('您容易大便干燥吗'))
                templateFun(tr_s, i, 6, 4, 2)
            else if (tr_s[i].innerText.includes('您舌苔厚腻或有舌苔厚厚的感觉吗'))
                templateFun(tr_s, i, 7, 1, 2)
            else if (tr_s[i].innerText.includes('您舌下静脉瘀紫或增粗吗'))
                templateFun(tr_s, i, 6, 0, 1)


        }
    }


    function zhongYi_2()
    {
        console.log("已进入-中医保健函数");


        // 外部获取 转诊的村医姓名
        let cun_doctor = get_cun_doctor();

        // 设定一个修改flag
        let cun_doctor_flag = false;


        let tr_s = $('tr');     // 找table中的一行tr
        for (let i = 0; i < tr_s.length; i++)
        {
            if (tr_s[i].innerText.includes('医生签名'))
            {

                let inputs = tr_s[i].getElementsByTagName("input");

                inputs[0].value = $.cookie("tiJianDate");
                inputs[0].dispatchEvent(fkVueEvent_change);

                let now_value = $.cookie("tiJianDate");
                let now_date = now_value.split("-", 3);
                now_date[0] = parseInt(now_date[0]) + 1;
                let new_now_date = now_date[0] + now_date[1] + now_date[2]
                console.log(new_now_date);
                inputs[1].value = new_now_date;
                inputs[1].dispatchEvent(fkVueEvent_change);


                console.log("进入中医保健 医生签名 模块");
                // 步骤一：模拟点击下拉框，触发事件，获取下拉数据；如不点击获取不到相应下拉数据
                let div_s = tr_s[i].getElementsByTagName("div");
                for (let j = 0; j < div_s.length; j++)
                {
                    if ("combobox" === div_s[j].getAttribute("role"))
                    {
                        // div_s[j].dispatchEvent(click_Event);     原生JS报错new ClickEvent构建错误
                        div_s[j].click();
                        break;  // 目的达到，结束内循环
                    }
                }


                // 步骤二：模拟点击选取对应村医生
                setTimeout(function ()
                {
                    let ul_s = $('ul[role="listbox"]');
                    for (let j = 0; j < ul_s.length; j++)
                    {
                        if (ul_s[j].innerText.includes('曹碑镇卫生院'))
                        {
                            let li_s = ul_s[j].getElementsByTagName("li");
                            for (let z = 0; z < li_s.length; z++)
                            {
                                // 关键：如果下拉列表中有村医 和 签约的村医一致，则点击该村医
                                if (li_s[z].innerText.includes(cun_doctor) && !cun_doctor_flag
                                    && !li_s[z].innerText.includes("禁") && !li_s[z].innerText.includes("停"))
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
    }


    function basicInfo()
    {
        console.log("已进入-基本信息修改");

        let edit_flag_job = false;


        let tr_s = $('tr');     // 找table中的一行tr
        for (let i = 0; i < tr_s.length; i++)
        {
            if (tr_s[i].innerText.includes('工作单位') && tr_s[i].innerText.includes('本人电话') && edit_flag_job === false)
            {
                edit_flag_job = true;
                let inputs = tr_s[i].getElementsByTagName("input");

                inputs[0].value = "务工";
                inputs[0].dispatchEvent(fkVueEvent);

            }
            else if (tr_s[i].innerText.includes('医疗费用') && tr_s[i].innerText.includes('支付方式'))
            {
                let divs = tr_s[i].getElementsByTagName("div");

                for (let k = 0; k < divs.length; k++)
                {
                    if (divs[k].innerText.includes('1城乡居民基本医疗保险') && !divs[k].className.includes('checked'))
                    {
                        divs[k].click();
                    }
                    if (divs[k].innerText.includes('3城镇居民基本医疗保险') && divs[k].className.includes('checked'))
                    {
                        divs[k].click();
                    }
                }
            }
        }
    }


    function pdfGetDATA()
    {
        // PDFJS.getDocument('https://eicore-invoice-24.s3.cn-north-1.jdcloud-oss.com/digital-invoice/digital_24947200000022571933.pdf?' +
        //     'AWSAccessKeyId=JDC_8007B4FE0EE6947B08A911AD2BAD&Expires=2679021790&Signature=L8HY4FQmVy2bPxb2TvcmT2RYR1M%3D');

        // getPdf('https://eicore-invoice-24.s3.cn-north-1.jdcloud-oss.com/digital-invoice/digital_24947200000022571933.pdf?' +
        //     'AWSAccessKeyId=JDC_8007B4FE0EE6947B08A911AD2BAD&Expires=2679021790&Signature=L8HY4FQmVy2bPxb2TvcmT2RYR1M%3D');

        const loadingTask = pdfjsLib.getDocument('https://file.ruifumedical.com/files/result/2024/12/16/W1100844060.pdf');

        loadingTask.promise.then(function (pdf)
        {
            // pdf is the loaded PDF document
            console.log("PDF loaded successfully:", pdf);

            // Access the number of pages
            console.log("Number of pages:", pdf.numPages);

            // Get a specific page
            pdf.getPage(1).then(function (page) {
                // page is the loaded page object
                console.log("Page 1 loaded:", page);
            });
        });


        console.log("Get in the pdfjs successfully.");
    }



    // 程序入口
    document.addEventListener("keydown", function (fuckEvent)
    {
        let useFlag = true;
        if (fuckEvent.key === "F9" && useFlag)
        {
            console.log("您已按下F9，实现弹窗，StartFunction");


            let DllButton = "";

            const Pre_DllButton = "<div id='fuck.this.shit' style='font-family: SimSun,fangsong; font-weight: bold; display: block; line-height: 22px; " +
                "text-align: center; vertical-align: center; background-color: #25ae84; cursor: pointer; margin: 2px; position: fixed; left: 0; top: 185px; width: 70px; z-index: 8888;'>";
            const Btm_DllButton = "</div>";

            const Br_String = "<div style='height: 4px;'></div>";

            const tiJian_String_1 = "<input id = 'tiJianDate' placeholder='体检日期' value='" + $.cookie("tiJianDate") + "' style='width: 70px; height: 22px; text-align:center; color: brown;'>";

            const tiJian_String_2 = "<a id='tiJian_a' target='_blank' style='font-size:15px; color:#fff; display: block; height: 100%; padding: 3px 1px;'" +
                " onmouseover=\"this.style.color='red'\" onmouseout=\"this.style.color='white'\">体检</a>";

            const suiFang_String = "<a id='zhuanzhen_a' target='_blank' style='font-size:15px; color:#fff; display: block; height: 100%; padding: 3px 1px;'" +
                " onmouseover=\"this.style.color='red'\" onmouseout=\"this.style.color='white'\">转诊</a>" +
                "<div style='height: 4px;'></div>" +
                "<a id='suiFangResult_a' target='_blank' style='font-size:15px; color:#fff; display: block; height: 100%; padding: 3px 1px;'" +
                " onmouseover=\"this.style.color='red'\" onmouseout=\"this.style.color='white'\">随访</a>";


            // const sfDayString = "<a id='sfDay_a' target='_blank' style='font-size:15px; color:#fff; display: block; height: 100%; padding: 3px 1px;'" +
            //     " onmouseover=\"this.style.color='red'\" onmouseout=\"this.style.color='white'\">sfDay</a>";
            //
            // const zhongYiString = "<a id='zhongYi_a' target='_blank' style='font-size:15px; color:#fff; display: block; height: 100%; padding: 3px 1px;'" +
            //     " onmouseover=\"this.style.color='red'\" onmouseout=\"this.style.color='white'\">中医</a>";
            //
            // const zhongYiString_2 = "<a id='zhongYi_a_2' target='_blank' style='font-size:15px; color:#fff; display: block; height: 100%; padding: 3px 1px;'" +
            //     " onmouseover=\"this.style.color='red'\" onmouseout=\"this.style.color='white'\">中医2</a>";
            //
            //
            // const basicInfoString = "<a id='basicInfo_a' target='_blank' style='font-size:15px; color:#fff; display: block; height: 100%; padding: 3px 1px;'" +
            //     " onmouseover=\"this.style.color='red'\" onmouseout=\"this.style.color='white'\">基信</a>";

            // Button_1 = + Br_String + sfDayString + Br_String + zhongYiString + Br_String + zhongYiString_2 + Br_String + basicInfoString;


            // const PDF_String = "<a id='PDF_a' target='_blank' style='font-size:15px; color:#fff; display: block; height: 100%; padding: 3px 1px;'" +
            //     " onmouseover=\"this.style.color='red'\" onmouseout=\"this.style.color='white'\">PDF</a>";

            DllButton = Pre_DllButton + tiJian_String_1 + Br_String + tiJian_String_2 + Br_String + suiFang_String + Br_String + Btm_DllButton;


            $("body").append(DllButton);

            if (tiJianDATE_Flag)
            {
                $("#tiJianDate")[0].addEventListener("focusout", function ()
                {
                    $.cookie('tiJianDate', $("#tiJianDate")[0].value, {expires: 365, path: '/'});
                    console.log("已完成日期cookie插入");
                });
            }

            $("#tiJian_a").click(function ()
            {
                tiJian();
            });

            $("#zhuanzhen_a").click(function ()
            {
                zhuanZhen();
            });

            $("#suiFangResult_a").click(function ()
            {
                suiFangResult();
            });

            $("#sfDay_a").click(function ()
            {
                sfDay();
            });

            $("#zhongYi_a").click(function ()
            {
                zhongYi();
            });

            $("#zhongYi_a_2").click(function ()
            {
                zhongYi_2();
            });

            $("#basicInfo_a").click(function ()
            {
                basicInfo();
            });



        }
    });

    // we have a test.




})();
