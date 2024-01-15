function fraction2decimal(m, n)
{
    let flag = true;

    let num = {};
    let i = 0;
    let x = parseInt(m / n);
    m = m % n;
    let result = "";
    while (m !== 0 && !(m in num))
    {
        num[m] = i++;
        result += parseInt(m * 10 / n);
        m = m * 10 % n;
    }
    if (m)
    {
        let index = num[m];
        flag = false;
        // return x + ". " + result.substring(0, index) + "( " + result.substring(index) + ") ";
    }
    if (flag)
        return n;
}


function Test()
{
    let Temp;
    for (let i = 0; i <= 1000; i++)
    {
        Temp = fraction2decimal(1000, i);
        if (Temp)
            console.log(Temp);
    }
    return Temp
}


console.log("Test");
console.log(Test());
