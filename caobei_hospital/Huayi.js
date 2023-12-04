// ==UserScript==
// @name         华医网考试助手
// @namespace    https://github.com/windosx
// @version      1.1.6
// @description  1️⃣跳过视频 2️⃣自动选择答案 3️⃣错误提示
// @author       WindOSX
// @license      MIT
// @match        *://*.91huayi.com/course_ware/course_ware_polyv.aspx?*
// @match        *://*.91huayi.com/pages/exam.aspx?*
// @match        *://*.91huayi.com/pages/exam_result.aspx?*
// @icon         https://cme44.91huayi.com/favicon.ico
// @connect      49.234.55.61
// @grant        GM_xmlhttpRequest
// @grant        GM_setValue
// @grant        GM_getValue
// @grant        unsafeWindow
// ==/UserScript==

(function() {
    'use strict';

    const $ = unsafeWindow.$;
    const endpoint = 'http://49.234.55.61:6868';
    const btnStyle = 'cursor:pointer;margin-top:3px;padding:5px 10px 5px 28px;background-color:rgb(132,213,253);color:white;border-radius:5px;background-image:url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAAXNSR0IArs4c6QAAApdJREFUWEfFl02ITlEYx3//nRVREykLFiiSokQpwiDKQoo0Kx9RCgsbFmYWzEaJBZuZksUoS5lEPsZXI8lGKVKmKNmhpGwePW/3fTvu3HPuuTNT71O3t/c+X//n/5zznHNFl0Vdzk8jAGbWC2wDNgDzi8dr+F48r4GnwJikHznFZQEwswPASWBdTlDgK3AFuCrpb8onCcDM5gDDwN7MxGWzt0CfpPcx/ygAM1sCPAcWTjF56LYiBqISgJktAL7NQOIwxCpJ78oxYwCeARszAHivvwCzgUXFb8xtAlgt6WdoMAmAmR0HriWSjwIjkkbKNmZ2FDgNLI/4D0k6EgVgZnOBcWBZJMALoFfSnxhAM/Mt+giYFbHZIulxW/cfA2Z2HuhPVL9e0qu23szmAQeBe5I+Be+HgEOROHck7YkBeAOsiTiOS/LqWmJmfcDN4u+wpMOBbh9wOxLH50KPpF+u7zBgZj5kOtVVODszDyW9LAD4pPM54TIhaXEA4BRwOcHkDkn3ywAuAGcTTqHqI7A0eNEvaSAA4Mw4QzG5KOlcGUCqbylclySdyaS/bdZpWdiCu8CuTAbaZuXKfeF5IXUyKml3mYGmAB5I2h5Ufh04Vpe50FcCaNqCQUmtNWNm+4FbmcndrLIFTRahB9ksaawA4FPRj+xcqVyEdduwHLyVPJBNudmByduwqCQ1iMrxyxMzNUFD3+pBVACoG8WdQJLCHeTVP8lkIDmK6w6jmQAQP4wKFuqO4xaIKTKQPo6DPZ17IclkvWWWdyEpWOjulawA0QP4xWFlkzIrbD8AOyV9ropT+11gZj5efcxORW4AJyT9jjnXAijYWAsMAlszUXi/ByQ5gKRkAQgWZ3c+zeqqmI6+EQPTSRTz/Qdck/ghLJUSFgAAAABJRU5ErkJggg==);background-size: 22px 22px;background-repeat:no-repeat;background-position: 4px 3px;';

    // 重新选择答案
    unsafeWindow.wrongAnswer = function(target) {
        var e = unsafeWindow.event;
        e.preventDefault();
        e.stopPropagation();
        $(target).parents('tr:eq(0)').siblings().find('input[type=radio]').removeAttr('disabled');
        $(target).parent().siblings('input:checked').removeAttr('checked');
        $(target).parents('td:eq(0)').removeAttr('style');
        $(target).parents('div:eq(0)').remove();
    }

    // 指定正确答案
    unsafeWindow.rightAnswer = function(target) {
        var e = unsafeWindow.event;
        e.preventDefault();
        e.stopPropagation();
        $(target).parents('td:eq(0)').removeAttr('style');
        $(target).parents('tr:eq(0)').siblings().find('div').remove();
        $(target).parents('tr:eq(0)').siblings().find('td').removeAttr('style');
        $(target).parents('tr:eq(1)').find('input[type=radio]').removeAttr('disabled');
        $(target).parents('td:eq(0)').find('input[type=radio]').attr('checked', true);
        $(target).parents('td:eq(0)').find('div').remove();
    }

    let usernameOrigin = $('#spName').text().trim();
    let username = usernameOrigin.substring(3, usernameOrigin.length - 4).trim();
    let cwid = location.href.substring(location.href.indexOf('cwid=') + 5);

    // 跳过视频
    if (unsafeWindow.s2j_onPlayOver) {
        unsafeWindow.s2j_onPlayOver();
    }

    // 答题界面流程
    let questionForm = $('form#form1');
    if (questionForm.length) {
        let questionElems = $('span[id^="gvQuestion_question_"');
        // 查询题库
        questionElems.each(function(idx, ele) {
            let questionId = $('input[id="gvQuestion_question_id_' + idx + '"]').val();
            GM_xmlhttpRequest({
                url: endpoint + '/api/v1/question/' + questionId,
                method: 'GET',
                responseType: 'json',
                onload: function(data) {
                    if (!!data.response) {
                        let question = data.response.data;
                        if (!question || !question.answers || !question.answers.length) return;
                        let hasCorrectAnswer = false;
                        let correctAnswerIdx = -1;
                        for (let i = 0; i < question.answers.length; i++) {
                            if (question.answers[i].correct) {
                                hasCorrectAnswer = true;
                                correctAnswerIdx = i;
                                break;
                            }
                        }
                        if (hasCorrectAnswer) {
                            let bingo = $('input[value="' + question.answers[correctAnswerIdx].id + '"]');
                            let parent = bingo.parent();
                            bingo.attr('checked', true);
                            parent.attr('style', 'background: rgba(0, 255, 0, .5)');
                            parent.append('<div style="display:inline-block;padding-left: 12px">✔ 自动选择（由用户【' + question.answers[correctAnswerIdx].updateUsername + '】提供答案）<button onclick="javascript:wrongAnswer(this)" style="' + btnStyle + '">答案有误</button></div>');
                            parent.parent().siblings().find('input[type=radio]').attr('disabled', true);
                        } else {
                            for (let i = 0; i < question.answers.length; i++) {
                                let wrongAnswer = $('input[value="' + question.answers[i].id + '"]');
                                let wrongAnswerParent = wrongAnswer.parent();
                                wrongAnswer.attr('disabled', true);
                                wrongAnswerParent.attr('style', 'background: rgba(255, 0, 0, .5)');
                                wrongAnswerParent.append('<div style="display:inline-block;padding-left: 12px">✕ 错误答案（由用户【' + question.answers[i].updateUsername + '】踩坑）<button onclick="javascript:rightAnswer(this)" style="' + btnStyle + '">这是正确答案</button></div>');
                            }
                        }
                    }
                }
            });
        });

        // 交卷时提交问题
        questionForm.on('submit', function() {
            let questions = [];
            let incomplete = false;
            questionElems.each(function(idx, ele) {
                let questionId = $('input[id="gvQuestion_question_id_' + idx + '"]').val();
                let question = $(ele).text().replace(/^[0-9]/g, '').replace(/^[、]/g, '');
                let ansEle = $('input[id^="gvQuestion_rbl_' + idx + '_"]:checked');
                if (ansEle.length <= 0) {
                    incomplete = true;
                    return;
                }
                questions.push({
                    id: questionId,
                    text: question,
                    username: username,
                    answer: {
                        id: $(ansEle).val(),
                        text: $(ansEle).siblings('label').text().replace(/^[A-Z]/g, '').replace(/^[、]/g, ''),
                        correct: true
                    }
                });
            });
            if (incomplete) return;
            GM_setValue('questions', JSON.stringify(questions));
        });
    }

    // 考试结束流程
    if ($('.tips_text').length <= 0) return;
    let questions = JSON.parse(GM_getValue('questions'));
    if ($('.tips_text').text() === '考试未通过') {
        $('.state_lis_text').each(function(idx, ele) {
            for (let i = 0; i < questions.length; i++) {
                if ($(ele).text() === questions[i].text) {
                    questions[i].answer.correct = false;
                }
            }
        });
    } else {
        for (let i = 0; i < questions.length; i++) {
            questions[i].answer.correct = true;
        }
    }
    const requestBody = {
        uid: cwid,
        username: username,
        questions: questions
    }
    GM_xmlhttpRequest({
        url: endpoint + '/api/v1/question',
        method: 'POST',
        data: JSON.stringify(requestBody),
        headers: { 'Content-Type': 'application/json' }
    });
})();