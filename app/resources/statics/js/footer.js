$(function(){
    renderFooter();
});


window.addEventListener("resize", (event) => {
    renderFooter();
});

function renderFooter() {
    document.getElementById('p-footer-copyright').innerHTML=`Copyright © ${String(new Date().getFullYear())} <a href="https://www.chtsecurity.com/" target="_blank"> CHT Security</a> Co., Ltd. All rights reserved.`;
}