//TODO: Figure out why toasts only work once per page?
function toast(text) {
    constructToast({
        html: text
    })
}

function toast(text, type) {
    constructToast({
        html: text,
        type: type
    })
}

function toast(text, type, time) {
    constructToast({
        html: text,
        type: type,
        time: time
    })
}

function constructToast(obj) {
    text = "None"
    type = "info"
    html = undefined
    time = 5000
    if (typeof obj.text !== 'undefined') {
        text = obj.text
    }
    if (typeof obj.type !== 'undefined') {
        type = obj.type
    }
    if (typeof obj.html !== 'undefined') {
        html = obj.html
    }
    if (typeof obj.time !== 'undefined') {
        time = obj.time
    }
    toastData = {
        class: "alert alert-" + type + " snackbar show"
    }
    if (typeof html !== 'undefined') {
        toastData['html'] = html
    } else {
        toastData['text'] = text
    }

    toast = jQuery('<div/>', toastData).appendTo("#toasts");
    setTimeout(function(){
        toast.addClass("hide")

        //TODO: occasionally there's a flicker
        setTimeout(function() {
            toast.remove();
        }, 600)
    }, time);
}
