const sites = [
    { name: '4KVM', url: 'https://www.4kvm.org', icon: '🎬' },
    { name: 'NoVipNoAd', url: 'https://www.novipnoad.net/', icon: '📺' },
    { name: 'YaNetflix', url: 'https://yanetflix.com', icon: '🎥' },
    { name: 'Libvio', url: 'https://www.libvio.site/', icon: '🎞️' },
    { name: 'VisionTV', url: 'https://www.visiontv.club/', icon: '🔮' },
    { name: 'DDYS', url: 'https://ddys.io/', icon: '🐉' }
];

const navGrid = document.getElementById('nav-grid');
const floatingHearts = document.getElementById('floating-hearts');

// 渲染卡片
sites.forEach(site => {
    const card = document.createElement('a');
    card.href = site.url;
    card.className = 'nav-card';
    card.target = '_blank';
    card.innerHTML = `
        <div class="icon">${site.icon}</div>
        <span>${site.name}</span>
    `;
    navGrid.appendChild(card);
});

// 生成背景漂浮爱心
function createHeart() {
    const heart = document.createElement('div');
    heart.className = 'floating-heart';
    heart.innerHTML = '❤️';
    heart.style.left = Math.random() * 100 + 'vw';
    heart.style.animationDuration = (Math.random() * 5 + 5) + 's';
    heart.style.fontSize = (Math.random() * 10 + 15) + 'px';
    floatingHearts.appendChild(heart);
    
    setTimeout(() => {
        heart.remove();
    }, 10000);
}

setInterval(createHeart, 800);
