document.onkeydown = function (event)
{
    // || arguments.callee.caller.arguments[0]
    const e = event || window.event;
    if (e.keyCode === 120)
    {
        console.log("You have pressed F9");

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
        inputs[38].value = '-';
        inputs[38].dispatchEvent(fkVueEvent_select);

        inputs[39].value = '+-';
        inputs[39].dispatchEvent(fkVueEvent_select);

        inputs[40].value = '+-';
        inputs[40].dispatchEvent(fkVueEvent_select);

        inputs[41].value = '+-';
        inputs[41].dispatchEvent(fkVueEvent_select);

        // 根据概率随机出现空腹、随机血糖
        const fkrate = Math.floor(Math.random() * (10 - 0 + 1)) + 0;
        if (fkrate < 5)
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
            if (divs[i].innerText === '2基本满意')
            {
                console.log('the div index=' + i)
                divs[i].click();
                console.log('已经勾选自我评估');
            }
            if (divs[i].innerText === '1粗筛阴性')
            {
                console.log('the div index=' + i)
                divs[i].click();
                console.log('已经勾选认知能力、情感状态');
            }
            if (divs[i].innerText === '1可自理（0~3分）')
            {
                console.log('the div index=' + i)
                divs[i].click();
                console.log('已经勾选认知能力、情感状态');
            }

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
    if (e.keyCode === 119)
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
}