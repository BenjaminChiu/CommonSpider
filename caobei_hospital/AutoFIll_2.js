document.addEventListener("keydown", function (fuckEvent)
{
    if (fuckEvent.key === "F9")
    {
        console.log("You have pressed F9");



        var oneInner = document.createElement("div");
        oneInner.setAttribute("style","background:#CC0000;position:absolute;z-index:9999;width:200px;height:150px;border:solid 3px #2F74A7;cursor:pointer;");

        var oneButton = document.createElement("input");
        oneButton.setAttribute("type","button");
        oneButton.setAttribute("class","btn btn-warning btn-sm");
        oneButton.setAttribute("style","float:right;");
        oneButton.setAttribute("value","x");
        oneInner.appendChild(oneButton);

        var oneSpan = document.createElement("span");
        oneSpan.setAttribute("style","word-break:break-all;white-space:normal;");
        oneSpan.innerHTML = "<font color='#FFFFFF'><br>&nbsp;&nbsp;&nbsp;&nbsp;新闻内容：<br>&nbsp;&nbsp;&nbsp;&nbsp;解决了悬浮框和轮播图优先级问题，上面是悬浮框，下面是轮播图，方法是：z-index:9999;</font>";
        oneInner.appendChild(oneSpan);

        document.body.appendChild(oneInner);




        let thefkingDate = prompt("请选择体检日期", "2023-02-24");
        console.log("检测到的输入为" + thefkingDate);

        const body_temperature = (Math.random() * (36.9 - 36) + 36).toFixed(1);
        //脉搏
        const pulse_rate = Math.floor(Math.random() * (82 - 68 + 1)) + 68;
        //呼吸频率
        const respiratory_rate = Math.floor(Math.random() * (21 - 16 + 1)) + 16;
        //高压
        const blood_pressure_high = Math.floor(Math.random() * (138 - 120 + 1)) + 120;
        //低压
        const blood_pressure_low = Math.floor(Math.random() * (88 - 72 + 1)) + 72;
        //高压
        const blood_pressure_high_2 = Math.floor(Math.random() * (138 - 120 + 1)) + 120;
        //低压
        const blood_pressure_low_2 = Math.floor(Math.random() * (88 - 72 + 1)) + 72;
        //血红蛋白
        const hemoglobin = Math.floor(Math.random() * (155 - 115 + 1)) + 115;
        //白细胞
        const hemameba = (Math.random() * (10 - 4) + 4).toFixed(2);
        //血小板
        const blood_platelet = Math.floor(Math.random() * (300 - 100 + 1)) + 100;
        //血糖
        const blood_sugar = (Math.random() * (6 - 4) + 4).toFixed(2);
        //高血糖 随机血糖
        const blood_sugar_high = (Math.random() * (12 - 6.2) + 6.2).toFixed(2);
        // 根据概率随机出现空腹、随机血糖
        const fkrate = Math.floor(Math.random() * (10 - 0 + 1)) + 0;


        // 只能获取单个input
        //const fk_inputs = document.getElementById('number');
        // fk_inputs.value = body_temperature;

        //获取所有input，根据index值进行操作
        const inputs = document.getElementsByTagName("input");


        // 解决vue页面注入js修改input值，
        // 只有当接收到键盘的按键(随便哪个键盘的按键消息)，才会触发input和change事件,进而把输入框中的value赋值给预设的相关变量，到这一步才算走完整个设置value的过程。
        // 所以如果想给这类加料的输入框或者选择框用原生JS赋值，设置vlaue属性过后就必须手动触发一下input或change事件。
        let fkVueEvent = document.createEvent('Event');
        fkVueEvent.initEvent("input", true, true);//如果是select选择框把"input"改成"change"
        fkVueEvent.eventType = 'message'

        let fkVueEvent_select = document.createEvent('Event');
        fkVueEvent_select.initEvent("change", true, true);//如果是select选择框把"input"改成"change"
        fkVueEvent_select.eventType = 'message'

        // 赋值操作，体温起手
        inputs[3].value = body_temperature;
        inputs[3].dispatchEvent(fkVueEvent);

        inputs[4].value = pulse_rate;
        inputs[4].dispatchEvent(fkVueEvent);

        inputs[5].value = respiratory_rate;
        inputs[5].dispatchEvent(fkVueEvent);

        inputs[6].value = blood_pressure_high;
        inputs[6].dispatchEvent(fkVueEvent);

        inputs[7].value = blood_pressure_low;
        inputs[7].dispatchEvent(fkVueEvent);

        inputs[8].value = blood_pressure_high_2;
        inputs[8].dispatchEvent(fkVueEvent);

        inputs[9].value = blood_pressure_low_2;
        inputs[9].dispatchEvent(fkVueEvent);

        // 血红蛋白
        inputs[35].value = hemoglobin;
        inputs[35].dispatchEvent(fkVueEvent);

        inputs[36].value = hemameba;
        inputs[36].dispatchEvent(fkVueEvent);

        inputs[37].value = blood_platelet;
        inputs[37].dispatchEvent(fkVueEvent);

        // 尿
        // inputs[38].value = '-';
        // inputs[38].dispatchEvent(fkVueEvent_select);
        //
        // inputs[39].value = '+-';
        // inputs[39].dispatchEvent(fkVueEvent_select);
        //
        // inputs[40].value = '+-';
        // inputs[40].dispatchEvent(fkVueEvent_select);
        //
        // inputs[41].value = '+-';
        // inputs[41].dispatchEvent(fkVueEvent_select);


        if (fkrate < 7)
        {
            // 空腹血糖 42
            inputs[42].value = blood_sugar;
            inputs[42].dispatchEvent(fkVueEvent);
        }
        else
        {
            // 随机血糖 43
            inputs[43].value = blood_sugar_high;
            inputs[43].dispatchEvent(fkVueEvent);
        }



        //获取所有input，根据index值进行操作
        const divs = document.getElementsByTagName("div");
        for (let i = 0; i < divs.length; i++)
        {
            if (divs[i].innerText === '2基本满意' && !divs[i].className.includes('checked'))
            {
                console.log('the div index=' + i)
                divs[i].click();
                console.log('已经勾选自我评估');
            }
            if (divs[i].innerText === '1粗筛阴性' && !divs[i].className.includes('checked'))
            {
                console.log('the div index=' + i)
                divs[i].click();
                console.log('已经勾选认知能力、情感状态');
            }
            // if (divs[i].innerText === '1可自理（0~3分）')
            // {
            //     console.log('the div index=' + i)
            //     divs[i].click();
            //     console.log('已经勾选认知能力、情感状态');
            // }

        }





        //获取table表中所有行
        const trs = document.getElementsByTagName("tr");
        for (let i = 0; i < trs.length; i++)
        {
            if (trs[i].innerText.includes("心电图"))
            {
                console.log("心电图tr的index=" + i)
                let trs_divs = trs[i].getElementsByTagName("div");
                for (let j=0; j<trs_divs.length; j++)
                {
                    if (trs_divs[j].innerText === "1正常")
                        trs_divs[j].click();
                }
                console.log('心电图已经完成操作！');
            }

            if (trs[i].innerText.includes("腹部B超"))
            {
                console.log("腹部B超tr的index=" + i)
                let trs_divs = trs[i].getElementsByTagName("div");
                for (let j=0; j<trs_divs.length; j++)
                {
                    if (trs_divs[j].innerText === "1正常")
                        trs_divs[j].click();
                }
                console.log('腹部B超已经完成操作！');
            }

            if (trs[i].innerText.includes("危险因素控制"))
            {
                console.log("危险因素控制tr的index=" + i)
                let trs_divs = trs[i].getElementsByTagName("div");
                for (let j=0; j<trs_divs.length; j++)
                {
                    if (trs_divs[j].innerText === "3饮食" && !trs_divs[j].className.includes('checked'))
                        trs_divs[j].click();
                    if (trs_divs[j].innerText === "4锻炼" && !trs_divs[j].className.includes('checked'))
                        trs_divs[j].click();
                    if (trs_divs[j].innerText === "6建议接种疫苗" && !trs_divs[j].className.includes('checked'))
                        trs_divs[j].click();
                    if (trs_divs[j].innerText === "7其他" && !trs_divs[j].className.includes('checked'))
                        trs_divs[j].click();
                }
                console.log('危险因素控制已经完成操作！');
            }
        }

        console.log("我尼玛为什么不执行了？？？")

        console.log("开始假装休眠")
        for (let i=0; i<10000; i++)
        {
            let the_one = (Math.random() * (36.9 - 36) + 36).toFixed(1);
            let the_two = (Math.random() * (36.9 - 36) + 36).toFixed(1);
            let the_tree = the_one * the_two;
        }



        //写建议
        let textarea_qt = document.getElementById('qtjy');
        textarea_qt.value = "预防骨质疏松与跌倒";
        textarea_qt.dispatchEvent(fkVueEvent_select);

        let textarea_ym = document.getElementById('jyjzym');
        textarea_ym.value = "流感疫苗、肺炎疫苗";
        textarea_ym.dispatchEvent(fkVueEvent_select);

        console.log("I am fucking down!")



    }

    // 用于弹窗的按键监听
    if (fuckEvent.key === "F8")
    {
        console.log("You have pressed F8");


        // 获取新产生 弹窗中的DIV，需要重新读取DIV
        const alert_divs = document.getElementsByTagName("div");
        for (let i=0; i<alert_divs.length; i++)
        {
            if (alert_divs[i].innerText.includes('0分') && alert_divs[i].innerText.includes('独立完成'))
            {
                alert_divs[i].click();
                console.log('弹窗DIV已点击！');
            }
        }


        // const buttons = document.getElementsByTagName("button");
        // for (let i=0; i<buttons.length; i++)
        // {
        //     if (buttons[i].innerText.includes("保 存"))
        //     {
        //         buttons[i].click();
        //         console.log("弹窗保存按钮已经点击！")
        //     }
        // }

    }


    // 代码暂存间
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

});

