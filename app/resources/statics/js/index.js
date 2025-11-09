function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
let cht_tip_csrf_token = getCookie('csrftoken');
let cht_tip_myHeaders = {};
cht_tip_myHeaders['X-CSRF-TOKEN'] = cht_tip_csrf_token;
$.ajaxSetup({
    headers: cht_tip_myHeaders
});

$(document).ajaxSend(function (e, xhr, options) {
    xhr.setRequestHeader('X-CSRFToken', cht_tip_csrf_token);
});




class Sidebar {
    constructor() {
        document.getElementById('sidebarCollapse').addEventListener("click", (event) => {
            document.getElementsByClassName('sidebar-header')[0].classList.toggle('collapse');
            document.getElementById('sidebar').classList.toggle('collapse');
            document.getElementsByClassName('content-page')[0].classList.toggle('collapse');
            document.getElementsByClassName('navbar')[0].classList.toggle('collapse');
            document.getElementsByClassName('page-footer')[0].classList.toggle('collapse');

            const collapse = localStorage.getItem('sidebar-collapse') === 'true';
            document.getElementById('collapse-icon').innerText = collapse ? 'menu_open' : 'menu';
            localStorage.setItem('sidebar-collapse', collapse ? 'false' : 'true');
        });

        document.getElementById('sidebar').addEventListener("mouseenter", (event) => {
            if (localStorage.getItem('sidebar-collapse') === 'true') {
                this.expend();
            }
        });

        document.getElementById('sidebar').addEventListener("mouseleave", (event) => {
            if (localStorage.getItem('sidebar-collapse') === 'true') {
                this.collapse();
            }
        });
    }

    collapse() {
        document.getElementsByClassName('sidebar-header')[0].classList.add('collapse');
        document.getElementById('sidebar').classList.add('collapse');
        document.getElementById('collapse-icon').innerText = 'menu';

        document.getElementsByClassName('content-page')[0].classList.add('collapse');
        document.getElementsByClassName('navbar')[0].classList.add('collapse');
        document.getElementsByClassName('page-footer')[0].classList.add('collapse');
    }

    expend() {
        document.getElementsByClassName('sidebar-header')[0].classList.remove('collapse');
        document.getElementById('sidebar').classList.remove('collapse');
        document.getElementById('collapse-icon').innerText = 'menu_open';

        document.getElementsByClassName('content-page')[0].classList.remove('collapse');
        document.getElementsByClassName('navbar')[0].classList.remove('collapse');
        document.getElementsByClassName('page-footer')[0].classList.remove('collapse');

    }
}

$(function () {
    // ui.Loading.start();
    // ui.Loading.stop();
    // ui.alert('test123');

    if (!localStorage.getItem('sidebar-collapse')) {
        localStorage.setItem('sidebar-collapse', 'false');
    }

    const sidebar = new Sidebar();

    if (localStorage.getItem('sidebar-collapse') === 'true') {
        sidebar.collapse();
    } else if (localStorage.getItem('sidebar-collapse') === 'false') {
        sidebar.expend();
    }

    if (!localStorage.getItem('dontshow-quickstart')) {
        localStorage.setItem('dontshow-quickstart', 'false');
    }

    if (localStorage.getItem('dontshow-quickstart') === 'false') {
        $('#quickstartModal').modal('show')
        localStorage.setItem('dontshow-quickstart', 'true');
    }
});

