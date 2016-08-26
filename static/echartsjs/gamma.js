/**
 * Created by kevin on 16/5/24.
 */
var memory_pure_increase = echarts.init(document.getElementById("memory_pure_increase"));
var disk_pure_increase = echarts.init(document.getElementById("disk_pure_increase"));

function get_memory_pure_increase(button) {
    memory_pure_increase.showLoading();
    $.get('/memory_pure_increase/', {'time_grading': button.name}).done(function (data) {
        var option = {
            title: {
                text: data['title'],
                subtext: '粒度包括最近12个月/最近15周/最近30天'
            },
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                data:data['legend'],
                selectedMode: 'single',
                selected: {
                    '存量': true
                }
            },
            toolbox: {
                show: true,
                feature: {
                    //dataZoom: {},
                    //dataView: {readOnly: false},
                    magicType: {type: ['bar', 'line']},
                    restore: {},
                    saveAsImage: {}
                }
            },
            xAxis:  {
                type: 'category',
                boundaryGap: false,
                data: data['xAxis']
            },
            yAxis: {
                type: 'value',
                axisLabel: {
                    formatter: '{value} 个'
                }
            },
            series: [
                {
                    name:'创建',
                    type:'line',
                    smooth:true,
                    data:data['data1'],
                    markLine: {
                        data: [
                            {type: 'average', name: '平均值'}
                        ]
                    },
                    label: {
                        normal: {
                            show: true,
                            position: 'top'
                        }
                    }
                },
                {
                    name:'删除',
                    type:'line',
                    smooth:true,
                    data:data['data2'],
                    markLine: {
                        data: [
                            {type: 'average', name: '平均值'}
                        ]
                    },
                    label: {
                        normal: {
                            show: true,
                            position: 'top'
                        }
                    }
                },
                {
                    name:'净增',
                    type:'line',
                    smooth:true,
                    data:data['data3'],
                    markLine: {
                        data: [
                            {type: 'average', name: '平均值'}
                        ]
                    },
                    label: {
                        normal: {
                            show: true,
                            position: 'top'
                        }
                    }
                },
                {
                    name:'存量',
                    type:'line',
                    smooth:true,
                    data:data['data4'],
                    //markLine: {
                    //    data: [
                    //        {type: 'average', name: '平均值'}
                    //    ]
                    //}
                    label: {
                        normal: {
                            show: true,
                            position: 'top'
                        }
                    }
                }
            ]
        };

        memory_pure_increase.hideLoading();
        memory_pure_increase.setOption(option);
    });
}
function get_disk_pure_increase(button) {
    disk_pure_increase.showLoading();
    $.get('/disk_pure_increase/', {'time_grading': button.name}).done(function (data) {
        var option = {
            title: {
                text: data['title'],
                subtext: '粒度包括最近12个月/最近15周/最近30天'
            },
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                data:data['legend'],
                selectedMode: 'single',
                selected: {
                    '存量': true
                }
            },
            toolbox: {
                show: true,
                feature: {
                    //dataZoom: {},
                    //dataView: {readOnly: false},
                    magicType: {type: ['bar', 'line']},
                    restore: {},
                    saveAsImage: {}
                }
            },
            xAxis:  {
                type: 'category',
                boundaryGap: false,
                data: data['xAxis']
            },
            yAxis: {
                type: 'value',
                axisLabel: {
                    formatter: '{value} 个'
                }
            },
            series: [
                {
                    name:'创建',
                    type:'line',
                    smooth:true,
                    data:data['data1'],
                    markLine: {
                        data: [
                            {type: 'average', name: '平均值'}
                        ]
                    },
                    label: {
                        normal: {
                            show: true,
                            position: 'top'
                        }
                    }
                },
                {
                    name:'删除',
                    type:'line',
                    smooth:true,
                    data:data['data2'],
                    markLine: {
                        data: [
                            {type: 'average', name: '平均值'}
                        ]
                    },
                    label: {
                        normal: {
                            show: true,
                            position: 'top'
                        }
                    }
                },
                {
                    name:'净增',
                    type:'line',
                    smooth:true,
                    data:data['data3'],
                    markLine: {
                        data: [
                            {type: 'average', name: '平均值'}
                        ]
                    },
                    label: {
                        normal: {
                            show: true,
                            position: 'top'
                        }
                    }
                },
                {
                    name:'存量',
                    type:'line',
                    smooth:true,
                    data:data['data4'],
                    //markLine: {
                    //    data: [
                    //        {type: 'average', name: '平均值'}
                    //    ]
                    //}
                    label: {
                        normal: {
                            show: true,
                            position: 'top'
                        }
                    }
                }
            ]
        };

        disk_pure_increase.hideLoading();
        disk_pure_increase.setOption(option);
    });
}

get_memory_pure_increase({'name': 'month'});
get_disk_pure_increase({'name': 'month'});