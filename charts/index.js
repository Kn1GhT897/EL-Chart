const fs = require('fs').promises
const puppeteer = require('puppeteer')

async function delay(time) {
    return new Promise((resolve) => {
        setTimeout(resolve, time)
    })
}

!(async () => {
    const browser = await puppeteer.launch({
        headless: true,
        ignoreDefaultArgs: ["--enable-automation"],
        defaultViewport: null,
    })
    const page = await browser.newPage()
    await page.evaluate(
        (data) => {
            window.__data__ = data
        },
        JSON.parse((await fs.readFile('data.json')).toString())
    )
    await page.evaluate(
        (source) => {
            document.write(source)
        },
        (await fs.readFile('chart.html')).toString()
    )
    await page.waitForFunction(() => window.__rendered__)
    await delay(3000)
    let chart = await page.screenshot({
        clip: {
            x: 0, y: 0, width: 380, height: 350
        }
    })
    await fs.writeFile('../chart.png', chart)
    await browser.close()
})()
