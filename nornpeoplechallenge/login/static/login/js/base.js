//** empty */

$(document).ready(function(){
    
    $("#filter-remove").on("click", function(){
        $(this).hide();
        $("#filter-date").val("");
        $("#filter-date-end").val("");
        //$("filter-all").val("");
        $("td").parent().show();
    });

    $("#filter-date").on("change",function (){
        let toFilter = $(this).val().toString(); /** format  2001-12-30 */
        $("#filter-remove").show();
        $(".LoginLogsTable tbody tr").filter(function() {
            $(this).toggle($(this).text().indexOf(toFilter) > -1)
        });
    });

    $("#filter-all").on("keyup", function(){
        let toFilter = $(this).val().toLowerCase();
        $(".LoginLogsTable tbody tr").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(toFilter) > -1)
        });
        
    });


});