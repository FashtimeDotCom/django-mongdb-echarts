/**
 * Created by kevin on 16/4/17.
 */
var topleft = echarts.init(document.getElementById('topleft'));
var topright = echarts.init(document.getElementById('topright'));
var top_10_industry = echarts.init(document.getElementById('top_10_industry'));
var one_one = echarts.init(document.getElementById('one_one'));
var one_two = echarts.init(document.getElementById('one_two'));

topleft.showLoading();
topright.showLoading();
top_10_industry.showLoading();
one_two.showLoading();
one_one.showLoading();

$.get('/topleft/').done(function (data) {
    var option = {
        title : {
            text: '外部DB类型与版本分布',
            //subtext: '纯属虚构',
            x:'center'
        },
        tooltip: {
            trigger: 'item',
            formatter: "{a} <br/>{b}: {c} ({d}%)"
        },
        legend: {
            orient: 'vertical',
            x: 'left',
            y: 'bottom',
            data: data['data']
        },
        series: [
            {
                name: '数据库类型',
                type: 'pie',
                selectedMode: 'single',
                radius: [0, '40%'],

                label: {
                    normal: {
                        position: 'inner'
                    }
                },
                labelLine: {
                    normal: {
                        show: false
                    }
                },
                data: data['data1']
            },
            {
                name: 'MySQL是否高可用',
                type: 'pie',
                radius: ['45%', '65%'],

                label: {
                    normal: {
                        position: 'inner'
                    }
                },

                data: data['data2']
            },
            {
                name: '数据库版本',
                type: 'pie',
                radius: ['70%', '80%'],

                data: data['data3'],
                itemStyle: {
                    normal: {
                        color: function(params) {
                            // 构建自己想要的颜色库
                            var colorList = ['#C1232B','#B5C334','#FCCE10', '#E87C25','#27727B','#FE8463','#9BCA63','#FAD860','#F3A43B','#60C0DD', '#D7504B','#C6E579','#F4E001','#F0805A','#26C0C0'];
                            return colorList[params.dataIndex]
                        }
                    }
                }
            }
        ]
    };
    topleft.setOption(option);
    topleft.hideLoading();
});

$.get('/topright/').done(function (data) {
    var option = {
        title : {
            text: '内部DB类型与版本分布',
            //subtext: '纯属虚构',
            x:'center'
        },
        tooltip: {
            trigger: 'item',
            formatter: "{a} <br/>{b}: {c} ({d}%)"
        },
        legend: {
            orient: 'vertical',
            x: 'left',
            y: 'bottom',
            data: data['data']
        },
        series: [
            {
                name: '数据库类型',
                type: 'pie',
                selectedMode: 'single',
                radius: [0, '40%'],

                label: {
                    normal: {
                        position: 'inner'
                    }
                },
                labelLine: {
                    normal: {
                        show: false
                    }
                },
                data: data['data1']
            },
            {
                name: 'MySQL是否高可用',
                type: 'pie',
                radius: ['45%', '65%'],

                label: {
                    normal: {
                        position: 'inner'
                    }
                },

                data: data['data2']
            },
            {
                name: '数据库版本',
                type: 'pie',
                radius: ['70%', '80%'],

                data: data['data3'],
                itemStyle: {
                    normal: {
                        color: function(params) {
                            // 构建自己想要的颜色库
                            var colorList = ['#C1232B','#B5C334','#FCCE10', '#E87C25','#27727B','#FE8463','#9BCA63','#FAD860','#F3A43B','#60C0DD', '#D7504B','#C6E579','#F4E001','#F0805A','#26C0C0'];
                            return colorList[params.dataIndex]
                        }
                    }
                }
            }
        ]
    };
    topright.setOption(option);
    topright.hideLoading();
});

$.get('/top_10_industry/').done(function (data) {
    var option = {
        title : {
            text: '行业前十',
            //subtext: '纯属虚构',
            x:'center'
        },
        tooltip: {
            trigger: 'item',
            formatter: "{a} <br/>{b}: {c} ({d}%)"
        },
        legend: {
            orient: 'vertical',
            x: 'left',
            y: 'bottom',
            data: data['data']
        },
        series: [
            {
                name: '行业',
                type: 'pie',
                selectedMode: 'single',
                radius: ['30%', '60%'],

                //label: {
                //    normal: {
                //        position: 'inner'
                //    }
                //},
                labelLine: {
                    normal: {
                        show: true
                    }
                },
                data: data['data1']
            },
            //{
            //    name: 'MySQL是否高可用',
            //    type: 'pie',
            //    radius: ['45%', '65%'],
            //
            //    label: {
            //        normal: {
            //            position: 'inner'
            //        }
            //    },
            //
            //    data: data['data2']
            //},
            //{
            //    name: '数据库版本',
            //    type: 'pie',
            //    radius: ['70%', '80%'],
            //
            //    data: data['data3'],
            //    itemStyle: {
            //        normal: {
            //            color: function(params) {
            //                // 构建自己想要的颜色库
            //                var colorList = ['#C1232B','#B5C334','#FCCE10', '#E87C25','#27727B','#FE8463','#9BCA63','#FAD860','#F3A43B','#60C0DD', '#D7504B','#C6E579','#F4E001','#F0805A','#26C0C0'];
            //                return colorList[params.dataIndex]
            //            }
            //        }
            //    }
            //}
        ]
    };
    top_10_industry.setOption(option);
    top_10_industry.hideLoading();
});




$.get('/one_one/').done(function (data) {
    var option = {
        // 例子：柱状图的每个柱子、饼图的每个扇形
        itemStyle: {
            // 正常展示下的样式
            normal: {
                color: 'green'
            },
            // 鼠标放上去的样式
            emphasis: {
                color: 'black'
            }
        },
        title: {
            text: data['title']
        },
        tooltip: {},
        legend: {
            data: ['数量']
        },
        xAxis: {
            data: data['field_list']
        },
        yAxis: {},
        series: [{
            name: data['series_name'],
            type: 'bar',
            data: data['count_list']
        }]
    };
    one_one.hideLoading();
    one_one.setOption(option);
});


$.get('/one_two/').done(function (data) {
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
    one_two.hideLoading();
    one_two.setOption(option);
});

// 绑定一个点击事件
one_one.on('click', function (params) {
    // 控制台打印数据的名称
    console.log(params);
    sweetAlert(params.name)
});



// 绑定一个点击事件,生成新的图表
top_10_industry.on('click', function (params) {
    // 控制台打印数据的名称
    console.log(params);
    var top_10_industry_further = echarts.init(document.getElementById('top_10_industry_further'));
    top_10_industry_further.showLoading();
    $.get('/top_10_industry_further/', {'Industry': params.name}).done(function (data) {
        var option = {
            title : {
                text: data['title'],
                //subtext: '纯属虚构',
                x:'center'
            },
            tooltip: {
                trigger: 'item',
                formatter: "{a} <br/>{b}: {c} ({d}%)"
            },
            legend: {
                orient: 'vertical',
                x: 'left',
                y: 'bottom',
                data: data['data']
            },
            series: [
                {
                    name: '数据库类型',
                    type: 'pie',
                    selectedMode: 'single',
                    radius: [0, '40%'],

                    label: {
                        normal: {
                            position: 'inner'
                        }
                    },
                    labelLine: {
                        normal: {
                            show: false
                        }
                    },
                    data: data['data1']
                },
                {
                    name: 'MySQL是否高可用',
                    type: 'pie',
                    radius: ['45%', '65%'],

                    label: {
                        normal: {
                            position: 'inner'
                        }
                    },

                    data: data['data2']
                },
                {
                    name: '数据库版本',
                    type: 'pie',
                    radius: ['70%', '80%'],

                    data: data['data3'],
                    itemStyle: {
                        normal: {
                            color: function(params) {
                                // 构建自己想要的颜色库
                                var colorList = ['#C1232B','#B5C334','#FCCE10', '#E87C25','#27727B','#FE8463','#9BCA63','#FAD860','#F3A43B','#60C0DD', '#D7504B','#C6E579','#F4E001','#F0805A','#26C0C0'];
                                return colorList[params.dataIndex]
                            }
                        }
                    }
                }
            ]
        };
        top_10_industry_further.setOption(option);
        top_10_industry_further.hideLoading();
    });
});