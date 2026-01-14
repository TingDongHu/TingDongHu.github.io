document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.highlight').forEach((block) => {
        // 1. 注入 Mac 圆点
        if (!block.querySelector('.mac-dots')) {
            const dots = document.createElement('div');
            dots.className = 'mac-dots';
            dots.innerHTML = '<span class="dot-red"></span><span class="dot-yellow"></span><span class="dot-green"></span>';
            block.prepend(dots);
        }

        // 2. 提取并注入语言
        const code = block.querySelector('code');
        if (code && !block.querySelector('.code-lang')) {
            const langMatch = code.className.match(/language-([a-z0-9+#]+)/i);
            if (langMatch) {
                const langLabel = document.createElement('span');
                langLabel.className = 'code-lang';
                langLabel.innerText = langMatch[1];
                block.appendChild(langLabel);
            }
        }

        // 3. 复制按钮
        if (!block.querySelector('.copy-btn')) {
            const btn = document.createElement('button');
            btn.className = 'copy-btn';
            btn.innerText = 'Copy';
            block.appendChild(btn);

            btn.addEventListener('click', () => {
                // 排除行号，只复制代码内容
                const codeLines = block.querySelectorAll('.lntd:last-child pre, pre:not(.lntd pre)');
                let text = "";
                codeLines.forEach(line => text += line.innerText);
                
                navigator.clipboard.writeText(text).then(() => {
                    btn.innerText = 'Copied!';
                    setTimeout(() => (btn.innerText = 'Copy'), 2000);
                });
            });
        }
    });
});