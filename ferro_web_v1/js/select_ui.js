
$('.sel').each(function() {
    $(this).children('select').css('display', 'none');

    var $current = $(this);

    $(this).find('option').each(function(i) {
        if (i == 0) {
            $current.prepend($('<div>', {
                class: $current.attr('class').replace(/sel/g, 'sel__box')
            }));

            let color_status = null;
            const attr = $(this).attr('data-color');
            if (typeof attr !== 'undefined' && attr !== false) {
                color_status = '_span_status_select_indicator _span_ssi_' + attr;
            }

            var placeholder = $(this).text();
            $current.prepend($('<span>', {
                class: $current.attr('class').replace(/sel/g, 'sel__placeholder ' + color_status),
                text: placeholder,
                'data-placeholder': placeholder
            }));

            return;
        }
        let color_status = null;
        const attr = $(this).attr('data-color');
        if (typeof attr !== 'undefined' && attr !== false) {
           color_status = '_span_status_select_indicator _span_ssi_' + attr;
        }

        $current.children('div').append($('<span>', {
            class: $current.attr('class').replace(/sel/g, 'sel__box__options '+ color_status),
            text:  $(this).text()
        }));
    });
});

// Toggling the `.active` state on the `.sel`.
$('.sel').click(function() {
    $(this).toggleClass('active');
});

// Toggling the `.selected` state on the options.
$('.sel__box__options').click(function() {
    var txt = $(this).text();
    var txt2 = $(this).html();
    var index = $(this).index();

    $(this).siblings('.sel__box__options').removeClass('selected');
    $(this).addClass('selected');

    var $currentSel = $(this).closest('.sel');
    $currentSel.children('.sel__placeholder').text(txt);
    console.log(txt2);
    $currentSel.children('select').prop('selectedIndex', index + 1);
    $currentSel.children('select').trigger("change");
});

$(function() {
    $("#" + $("#select_graph option:selected").val()).show();
    $("#select_graph").change(function(){
        $("._block_change_doom_sel").hide();
        $("#" + $(this).val()).show();
    });
});

document.getElementById("img_main").addEventListener("change", function () {
    if (this.files[0]) {
        var fr = new FileReader();

        fr.addEventListener("load", function () {
            document.getElementById("label_img").style.backgroundImage = "url(" + fr.result + ")";
        }, false);

        fr.readAsDataURL(this.files[0]);
    }
});
