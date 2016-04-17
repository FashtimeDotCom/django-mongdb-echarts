/**
 * Created by kevin on 16/4/17.
 */

var lefttop = echarts.init(document.getElementById('lefttop'));
var righttop = echarts.init(document.getElementById('righttop'));

righttop.showLoading();
lefttop.showLoading();

$.get('/lefttop/').done(function (data) {
    var option = {
        title: {
            text: data['title']
        },
        tooltip: {},
        legend: {
            data: ['数量']
        },
        xAxis: {
            //data: ["衬衫","羊毛衫","雪纺衫","裤子","高跟鞋","袜子"]
            data: data['field_list']
        },
        yAxis: {},
        series: [{
            name: data['series_name'],
            type: 'bar',
            //data: [5, 20, 36, 10, 10, 20]
            data: data['count_list']
        }]
    };
    lefttop.hideLoading();
    lefttop.setOption(option);
});

$.get('/righttop/').done(function (data) {
    var option = {
        title: {
            text: data['title']
        },
        tooltip: {},
        legend: {
            data: ['数量']
        },
        xAxis: {
            //data: ["衬衫","羊毛衫","雪纺衫","裤子","高跟鞋","袜子"]
            data: data['field_list']
        },
        yAxis: {},
        series: [{
            name: data['series_name'],
            type: 'bar',
            //data: [5, 20, 36, 10, 10, 20]
            data: data['count_list']
        }]
    };
    righttop.hideLoading();
    righttop.setOption(option);
});
lefttop.on('click', function (params) {
    // 控制台打印数据的名称
    console.log(params);
    sweetAlert(params.name)
});