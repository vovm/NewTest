$(document).ready(function() {
    function block_form() {
        $('textarea').attr('disabled', 'disabled');
        $('input').attr('disabled', 'disabled');
        $('#load').show();
    }

    function unblock_form() {
        $('textarea').removeAttr('disabled');
        $('input').removeAttr('disabled');
        $('#load').hide();
    }

    var options = {
        beforeSubmit: function(form, options) {
            block_form();
        },
        success: function() {
            unblock_form();
            $("#result").show();
            setTimeout(function() {
                $("#result").hide();
            }, 4000);
        }
    };

    $('#myForm').ajaxForm(options);

    function readURL() {
        var input = this;
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $(".image1").attr('src', e.target.result);
            }
            reader.readAsDataURL(input.files[0]);}}

    $(function () {
        $("#id_image").change(readURL)})
});
