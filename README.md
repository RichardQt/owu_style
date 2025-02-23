# 【CDN加速地址】：
``` html
https://jsdelivr.240723.xyz/gh/RichardQt/owu_style
```
---
# 【openwebui 美化】实现 Open-webui 代码框的自动折叠、mac 样式代码块，修改 open WebUI 字体样式。

source_url: https://linux.do/t/topic/440439
---

> 总觉得 openWebUI 代码框样式丑丑的，而且如果 ai 回复的代码长上下文多了后查看历史记录总是滑动的很累，而且看起来也很乱。遂美化一下，顺便把主要字体也改了。需要的话可以参考我下面的教程。

 - 话不多说先上效果图：
 light 模式：
 [![image](https://linux.do/uploads/default/optimized/4X/1/1/2/1124ad09dd6173ca893b9f06d22d062594391b4a_2_569x500.jpeg)
image1920×1686 125 KB](https://linux.do/uploads/default/1124ad09dd6173ca893b9f06d22d062594391b4a)
 dark 模式：
 [![1](https://linux.do/uploads/default/optimized/4X/7/0/f/70fd8435bc914ad105996ef15d10d6bd10e3415a_2_690x451.jpeg)
11920×1257 86.9 KB](https://linux.do/uploads/default/70fd8435bc914ad105996ef15d10d6bd10e3415a)
 简单改了下代码配色，mac 代码框样式，变量函数名斜体等，建议 operator mono、DankMono 等代码字体
 ![33](https://linux.do/uploads/default/original/4X/8/8/c/88c4d62a692e0ffb48a5c07994202b3377698466.gif)

 展开和折叠其实挺丝滑的，gif 看着有点卡。支持代码块内滑动浏览代码
 - **使用 custom.js、custom.css 方式注入不修改 openWebUI 原有代码**
 - **应该兼容 Chrome、Safari、Firefox、edge，适配 openWebUI 版本：v0.5.14 及以上版本**

## [](#p-4059527-h-1)教程

> 我是使用 Duplicate [@coker::](/u/coker) 佬的 huggingface space 来部署 openWebUI 的，下面教程适用于 huggingface space 以及 docker 方式来部署 openWebUI 的，其它方式可以参考。

 1. 上传 font 文件。（需要两种字体，代码块字体、openWebUI 主要字体）

 - 对于不使用 cdn 做静态资源加速的将你的字体放在 `fonts` 目录中，上传至 Dockerfile 的同级目录下
 - 对于使用 cdn 做静态资源加速的，上传至你的静态资源服务上即可。我是使用 cloudflare 大善人的 R2 来做静态存储的，并开启缓存。
 2. `custom.css`

 - 对于不使用 cdn 做静态资源加速的，请拷贝下面 `custom.css` 上传至 Dockerfile 的同级目录下，并修改字体名为你要使用的字体名。例如：
 `src: url('../assets/fonts/Jetbrains-Mono.woff2') format('woff2');`
 前面的路径不变。
 - 对于希望将 custom.css、custom.js、font 等静态资源上传至静态资源服务做加速的，请将 custom.css 放在你的静态资源服务器中。并修改 css 文件中的 `src: url('你的静态资源地址')`
 - 说明：

 `custom.css` 中我引入了三个 `font-face `，请根据你上传使用的字体进行修改，并修改 `body` 和`.cm-content` 的样式中 `font-family` 为你要使用的字体名。
 `body` 中的为 openWebUI 主要字体，`.cm-content` 中的为代码块中的字体。
 不会的可以留言或者问 ai。 可以根据喜好自行修改。推荐使用 woff2 字体，如果没有 woff2 字体文件，可以 Google 搜索在线字体转换，由于部分字体版权问题或者字体本身并不开源我这里就不提供字体。

 我上面使用的是 `DankMono` 作为代码块字体支持斜体样式，钉钉进步体作为 openWebUI 主要字体，搜一下都很好下载。
 ``` css
@font-face { font-family: 'Dank Mono'; src: url('https://image.coderman.site/webui/src/DankMono-Regular.woff2') format('woff2'); font-display: swap; font-style: normal; } @font-face { font-family: 'Dank Mono'; src: url('https://image.coderman.site/webui/src/DankMono-Italic.woff2') format('woff2'); font-display: swap; font-style: italic; } @font-face { font-family: 'JinBuTi'; src: url('https://image.coderman.site/webui/src/DingTalk-JinBuTi.woff2') format('woff2'); font-display: swap; } html { scroll-behavior: smooth; } body { font-family: 'JinBuTi', -apple-system, BlinkMacSystemFont, sans-serif; } /* 代码块容器样式 */ .language-javascript, [class*="language-"] { background: #f6f8fa !important; border-radius: 10px !important; box-shadow: 0 10px 30px 0 rgba(0, 0, 0, 0.1) !important; position: relative; margin: 1.2em 0; } .dark .language-javascript, .dark [class*="language-"] { background: #282c34 !important; box-shadow: 0 10px 30px 0 rgba(0, 0, 0, .4) !important; } /* 代码块顶部栏 */ .sticky.top-8 { background: #e1e4e8 !important; height: 40px !important; display: flex; align-items: center; border-radius: 10px 10px 0 0; padding: 0 15px !important; margin-bottom: -59px !important; } .dark .sticky.top-8 { background: #21252b !important; } /* 语言标识 */ .text-text-300 { position: absolute; left: 60px; top: 2px; color: #abb2bf !important; font-size: 17px !important; font-weight: 500 !important; z-index: 11; } .dark .text-text-300 { color: #586069 !important; } /* 顶部按钮样式优化 */ .save-code-button, .copy-code-button, .run-code-button { background: #f8f9fa !important; color: #333 !important; border: 1px solid #d1d5da !important; font-size: 12px !important; padding: 4px 12px !important; border-radius: 4px !important; transition: all 0.2s ease-in-out !important; } .dark .save-code-button, .dark .copy-code-button, .dark .run-code-button { background: #323842 !important; color: #abb2bf !important; border: 1px solid #3e4451 !important; } .save-code-button:hover, .copy-code-button:hover { background: #e9ecef !important; color: #222 !important; } .dark .save-code-button:hover, .dark .copy-code-button:hover { background: #3e4451 !important; color: #fff !important; } /* 代码块顶部装饰圆点 */ .language-javascript::before, [class*="language-"]::before { content: " "; position: absolute; border-radius: 50%; background: #ff5f56; width: 12px; height: 12px; left: 15px; top: 14px; box-shadow: 20px 0 #ffbd2e, 40px 0 #27c93f; z-index: 10; } .dakr .language-javascript::before, .dakr [class*="language-"]::before { background: #fc625d; box-shadow: 20px 0 #fdbc40, 40px 0 #35cd4b; } /* 代码内容区域 */ .cm-content { font-family: 'Dank Mono', -apple-system, BlinkMacSystemFont, Inter, ui-sans-serif, system-ui, 'Segoe UI', Roboto, Ubuntu, Cantarell, 'Noto Sans', sans-serif, 'Helvetica Neue', Arial, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', 'Noto Color Emoji'; font-size: 15px !important; line-height: 1.6em !important; padding: 20px 1.4em 1em 30px !important; color: #24292e !important; } .dark .cm-content { color: #abb2bf !important; } /* 代码语法高亮 */ .cm-line .ͼb { /* 关键字 */ color: #d73a49 !important; } .dark .cm-line .ͼb { color: #c678dd !important; } .cm-line .ͼd { /* 数字 */ color: #a29bfe !important; } .dakr .cm-line .ͼd { color: #e5c07b !important; } .cm-line .ͼe { /* 字符串 */ color: #6a89cc !important; } .dakr .cm-line .ͼe { color: #98c379 !important; } .cm-line .ͼg { /* 变量 */ color: #2ca9e1 !important; font-style: italic; } .dakr .cm-line .ͼg { color: #e3adb9 !important; } /* 代码语法高亮 - 扩展 */ .cm-comment { /* 注释 */ color: #7f848e !important; font-style: italic; } .cm-property { color: #61afef !important; } cm-tag { color: #e06c75 !important; } .cm-attribute { color: #d19a66 !important; } .cm-string { color: #98c379 !important; } .cm-operator { color: #56b6c2 !important; } span.ͼc { color: #7d5fff !important; } span.ͼl { color: #6bddcd !important; } span.ͼt { /* 暗色模式下的逗号 */ color: #ddb078 !important; ; font-style: italic; } span.ͼr { /* 暗色模式下的函数名 */ font-style: italic; } span.ͼf { /* 亮色模式下奇怪的符号 */ color: #70a1ff; } span.ͼm { /* 亮色模式下的注释 */ color: #f29a76; font-style: italic; } span.ͼw { /* 暗色模式下的注释 */ font-style: italic; } /* 滚动条样式 */ .cm-scroller::-webkit-scrollbar { height: 10px !important; width: 10px !important; background-color: #f6f8fa !important; } .dark .cm-scroller::-webkit-scrollbar { background-color: #282c34 !important; } .cm-scroller::-webkit-scrollbar-track { box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.1) !important; border-radius: 10px !important; background-color: #f6f8fa !important; } .dark .cm-scroller::-webkit-scrollbar-track { box-shadow: inset 0 0 6px rgba(0, 0, 0, .3) !important; background-color: #282c34 !important; } .cm-scroller::-webkit-scrollbar-thumb { border-radius: 10px !important; box-shadow: inset 0 0 6px rgba(0, 0, 0, .2) !important; background-color: #d1d5da !important; } .dark .cm-scroller::-webkit-scrollbar-thumb { box-shadow: inset 0 0 6px rgba(0, 0, 0, .5) !important; background-color: #3e4451 !important; } /* 行号栏样式 */ .cm-gutters { background: #f6f8fa !important; border-right: 1px solid #d1d5da !important; color: #586069 !important; padding-right: 10px !important; } .dark .cm-gutters { background: #282c34 !important; border-right: 1px solid #3e4451 !important; color: #495162 !important; } /* 当前行高亮 */ .cm-activeLine { background: #6699ff0b !important; } .cm-gutterElement.cm-activeLineGutter { background-color: #f9d3e3; } .dark .cm-gutterElement.cm-activeLineGutter { background-color: #dd7694; } /* 添加代码选中样式 */ .cm-selectionBackground, .cm-content ::selection { background-color: rgba(122, 129, 255, 0.2) !important; } .cm-line.cm-selected { background-color: rgba(122, 129, 255, 0.2) !important; } /* 选中时的文本颜色保持原样，确保可读性 */ .cm-content ::selection { color: rgba(62, 158, 111, 0.9) !important; } .dark .cm-content ::selection { color: rgba(245, 177, 255, 0.9) !important; } /* 匹配相同结果时的颜色 */ .cm-selectionMatch { background-color: #9c88ff5a !important; } /* 当有多行选中时的样式 */ .cm-selectionLayer>.cm-selectionBackground { background-color: rgba(122, 129, 255, 0.2) !important; } /* 代码块折叠/展开样式添加与修改 */ .cm-scroller { padding-bottom: 40px; background-color: #f6f8fa; } .dark .cm-scroller { background-color: #282c34; } .cm-scroller { overflow: auto !important; } .cm-editor { transition: height 1s cubic-bezier(0.4, 0, 0.2, 1); overflow: hidden !important; } /* 只给超高的代码块添加最大高度和内边距 */ .cm-editor#collapsed { height: 400px; } /* .cm-editor#expanded { padding-bottom: 40px; } */ .code-expand-btn { position: absolute; bottom: 10px; left: 50%; transform: translateX(-50%); display: flex; justify-content: center; align-items: center; padding: 6px 15px; border-radius: 15px; font-size: 12px; cursor: pointer; border: none; color: #666; background: rgba(255, 255, 255, 0.6); backdrop-filter: blur(8px); box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); -webkit-backdrop-filter: blur(8px); z-index: 11; transition: all 0.3s ease; } .dark .code-expand-btn { background: rgba(45, 45, 45, 0.6); color: #fff; } .code-expand-btn:hover { background: rgba(255, 255, 255, 0.8); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); transform: translateX(-50%) translateY(-2px); box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15); } .dark .code-expand-btn:hover { background: rgba(45, 45, 45, 0.8); } .code-expand-btn:active { transform: translateX(-50%) translateY(0); box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); } .code-expand-btn::before { content: "⌄"; display: inline-block; margin-right: 4px; font-size: 14px; transition: transform 0.3s ease; } .code-expand-btn#expanded::before { transform: rotate(180deg); } .code-expand-btn::after { content: "展开代码"; } .code-expand-btn#expanded::after { content: "收起代码"; } /* 渐变遮罩 */ .cm-editor#collapsed::after { content: ''; position: absolute; bottom: 0; left: 0; right: 0; height: 100px; background: linear-gradient(transparent 0%, rgba(255, 255, 255, 0.3) 40%, rgba(255, 255, 255, 0.6) 80%, rgba(255, 255, 255, 0.8) 100%); pointer-events: none; opacity: 0; transition: opacity 0.3s ease; z-index: 10; /* 确保遮罩层覆盖到滚动条 */ width: calc(100% + 17px); /* 17px是标准滚动条宽度 */ } .dark .cm-editor#collapsed::after { background: linear-gradient(transparent 0%, rgba(45, 45, 45, 0.3) 40%, rgba(45, 45, 45, 0.6) 80%, rgba(45, 45, 45, 0.8) 100%); } /* 只在折叠状态显示渐变遮罩 */ .cm-editor#collapsed::after { opacity: 1; } 
 ```
 3. `custom.js`

 - 对于不使用 cdn 做静态资源加速的，请拷贝下面 `custom.js` 上传至 Dockerfile 的同级目录下
 - 对于使用 cdn 做静态资源加速的，请拷贝下面 `custom.js` 上传至你的静态资源服务
 - 下面压缩了代码，需要查看源码可自行格式化。
 - ``` js
   (function () { function checkIsEditPage() { return window.location.href.includes('/functions'); } let isCurrentlyEditPage = checkIsEditPage(); function onRouteChange() { isCurrentlyEditPage = checkIsEditPage(); if (isCurrentlyEditPage) { if (mutationObserverActive) { mutationObserver.disconnect(); mutationObserverActive = false; } } else { initializeAllCodeBlocks(); if (!mutationObserverActive) { mutationObserver.observe(document.body, { childList: true, subtree: true }); mutationObserverActive = true; } } } const originalPushState = history.pushState; history.pushState = function (state, title, url) { originalPushState.apply(history, arguments); onRouteChange(); }; window.addEventListener('popstate', onRouteChange); const observedCodeBlocks = new WeakSet(); const resizeObserver = new ResizeObserver((entries) => { if (isCurrentlyEditPage) return; for (const entry of entries) { const editorRoot = entry.target; if (!editorRoot.classList.contains('cm-editor')) continue; updateCodeBlock(editorRoot); } }); function updateCodeBlock(editorRoot) { if (editorRoot.querySelector('.code-expand-btn')) return; const height = editorRoot.scrollHeight; if (height > 400) { editorRoot.id = 'collapsed'; const expandBtn = document.createElement('button'); expandBtn.className = 'code-expand-btn'; expandBtn.id = 'collapsed'; editorRoot.appendChild(expandBtn); editorRoot.style.height = '400px'; } } function initializeCodeBlock(editorRoot) { if (observedCodeBlocks.has(editorRoot)) return; observedCodeBlocks.add(editorRoot); resizeObserver.observe(editorRoot); updateCodeBlock(editorRoot); } function initializeAllCodeBlocks() { if (isCurrentlyEditPage) return; document.querySelectorAll('.cm-editor').forEach(initializeCodeBlock); } const mutationObserver = new MutationObserver((mutations) => { if (isCurrentlyEditPage) return; let hasNewCodeBlocks = false; mutations.forEach((mutation) => { mutation.addedNodes.forEach((node) => { if (node.nodeType !== 1) return; if (node.classList?.contains('cm-editor')) { initializeCodeBlock(node); hasNewCodeBlocks = true; } else { const matches = node.querySelectorAll?.('.cm-editor') || []; matches.forEach((el) => { initializeCodeBlock(el); hasNewCodeBlocks = true; }); } }); }); if (hasNewCodeBlocks) requestAnimationFrame(initializeAllCodeBlocks); }); let mutationObserverActive = false; document.addEventListener('click', function (evt) { if (!evt.target.classList.contains('code-expand-btn')) return; const editorRoot = evt.target.closest('.cm-editor'); if (!editorRoot) return; const isCollapsed = editorRoot.id === 'collapsed'; requestAnimationFrame(() => { if (isCollapsed) { const scroller = editorRoot.querySelector('.cm-scroller'); editorRoot.style.height = `${scroller.scrollHeight}px`; editorRoot.id = 'expanded'; evt.target.id = 'expanded'; } else { editorRoot.style.height = '400px'; editorRoot.id = 'collapsed'; evt.target.id = 'collapsed'; const scrollTarget = editorRoot.closest('.relative.my-2')?.parentElement; scrollTarget?.scrollIntoView({ behavior: 'smooth', block: 'start' }); } }); }); function init() { isCurrentlyEditPage = checkIsEditPage(); if (!isCurrentlyEditPage) initializeAllCodeBlocks(); mutationObserver.observe(document.body, { childList: true, subtree: true }); mutationObserverActive = true; } if (document.readyState === 'loading') { document.addEventListener('DOMContentLoaded', init); } else { init(); } window.addEventListener('error', (error) => { console.error('Code block error:', error); }); window.addEventListener('unhandledrejection', (event) => { console.error('Unhandled rejection:', event.reason); }); })();
   ```
  
 4. Dockerfile

 在 `COPY sync_data.sh sync_data.sh` 这一行前面加入以下代码

 - 对于不使用 cdn 做静态资源加速的：
 - ```
   # 复制字体文件 COPY fonts/* /app/build/assets/fonts/ # 复制自定义CSS和JS文件 COPY custom.css /app/build/assets/ COPY custom.js /app/build/assets/ # 在标签前添加custom.css引用 RUN sed -i 's|||' /app/build/index.html && \ sed -i 's|||' /app/build/index.html
   ```
 - 放在静态资源服务的，替换为你的 `custom.js`、`custom.css` 资源地址：
 - ```
   # 在标签前添加custom.css引用 RUN sed -i 's|||' /app/build/index.html && \ sed -i 's|||' /app/build/index.html 
   ```
  这样就完成了美化，如果你要修改 openWebUI 背景图片，建议还是上传至静态资源托管使用 cdn 链接，否则 openWebUI 将会以 base64 的方式嵌入 html 进行访问，很是拖慢速度。
  ``` shell
curl -X POST "{opneweburl}/api/v1/users/user/settings/update" \ -H "Authorization: Bearer token" \ -H "Content-Type: application/json" \ -d '{"ui": {"backgroundImageUrl": "https://你的背景图片地址"}}' 
  ```
  
  其中 Bearer token 为 设置 -> 账号 ->JWT 令牌

| 日期 | 更新内容 |
|:---|:---|
| 2.23 | 增加 light 模式，重新复制 custom.css 替换即可 |
