var notify_badge_class;
var notify_menu_class;
var notify_api_url;
var notify_fetch_count;
var notify_unread_url;
var notify_mark_all_unread_url;
var notify_refresh_period = 15000;
var consecutive_misfires = 0;
var registered_functions = [];
var count = 0

function fill_notification_badge(data) {
    var badges = document.getElementsByClassName(notify_badge_class);
    if (badges) {
        for (var i = 0; i < badges.length; i++) {
            badges[i].innerHTML = data.unread_count;
        }
    }
}

function fill_notification_list(data) {


    var main = document.getElementById("notif-menu")

    main.innerHTML = ""
    for (var i = 0; i < data.unread_list.length; i++) {

        var divide = document.createElement("div")
        divide.classList = "dropdown-divider"


        var media = document.createElement("div")
        media.classList = "media"

        var mediaBody = document.createElement("div")
        mediaBody.classList = "media-body"

        var h3 = document.createElement("h3")
        h3.classList = "dropdown-item-title"
        h3.style = "text-align: center"
        h3.innerText = data.unread_list[i].actor

        var span = document.createElement("span")
        span.classList = "float-right text-sm text-danger"

        h3.appendChild(span)


        var p1 = document.createElement("p")
        p1.classList = "text-sm"
        p1.style = "text-align: center"
        p1.innerText = data.unread_list[i].description

        var p2 = document.createElement("p")
        p2.classList = "text-sm text-muted"
        p2.style = "text-align: center"
        p2.innerText = data.unread_list[i].natural_time
        var i_ = document.createElement("i")
        i_.classList = "far fa-clock mr-1"
        p2.appendChild(i_)

        mediaBody.appendChild(h3)
        mediaBody.appendChild(p1)
        mediaBody.appendChild(p2)
        media.appendChild(mediaBody)
        main.appendChild(media)
        main.appendChild(divide)
    }
    var aTag = document.createElement("a")
    aTag.href = "/users/email-response/"
    aTag.classList = "dropdown-item dropdown-footer"
    aTag.innerText = "See All Email Responses"
    main.appendChild(aTag)

    if (data.unread_count > count) {
        var x = document.getElementById("popUp");
        x.className = "show";
        setTimeout(function () {
            x.className = x.className.replace("show", "");
        }, 2000);
        count = data.unread_count
    }
    console.log(count, 'xxx')

}

function register_notifier(func) {
    registered_functions.push(func);
}

function fetch_api_data() {
    if (registered_functions.length > 0) {
        //only fetch data if a function is setup
        var r = new XMLHttpRequest();
        r.addEventListener('readystatechange', function (event) {
            if (this.readyState === 4) {
                if (this.status === 200) {
                    consecutive_misfires = 0;
                    var data = JSON.parse(r.responseText);
                    for (var i = 0; i < registered_functions.length; i++) {
                        registered_functions[i](data);
                    }
                } else {
                    consecutive_misfires++;
                }
            }
        })
        r.open("GET", notify_api_url + '?max=' + notify_fetch_count, true);
        r.send();
    }
    if (consecutive_misfires < 10) {
        setTimeout(fetch_api_data, notify_refresh_period);
    } else {
        var badges = document.getElementsByClassName(notify_badge_class);
        if (badges) {
            for (var i = 0; i < badges.length; i++) {
                badges[i].innerHTML = "!";
                badges[i].title = "Connection lost!"
            }
        }
    }
}

setTimeout(fetch_api_data, 1000);
