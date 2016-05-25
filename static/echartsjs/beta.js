/**
 * Created by kevin on 16/5/24.
 */

// 绑定一个点击事件,生成新的图表

var modal_company = UIkit.modal("#modal-1",{bgclose:false});
var modal_industry = UIkit.modal("#modal-2",{bgclose:false});

// 行业前十模态
top_10_industry.on('click', function (params) {
    // 控制台打印数据的名称
    console.log(params);
    if (params.data.selected) {
        modal_industry.show();
        var top_10_industry_further = echarts.init(document.getElementById('top_10_industry_further'));
        var top_10_industry_further2 = echarts.init(document.getElementById('top_10_industry_further2'));
        top_10_industry_further.showLoading();
        top_10_industry_further2.showLoading();
        $.get('/top_10_industry_count_further/', {'Industry': params.name}).done(function (data) {
            var option = {
                title: {
                    text: data['title'] + "行业DB类型与版本分布",
                    //subtext: '纯属虚构',
                    x: 'left',
                    textStyle: {
                        fontSize: 10
                    }
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
                                color: function (params) {
                                    // 构建自己想要的颜色库
                                    var colorList = ['#C1232B', '#B5C334', '#FCCE10', '#E87C25', '#27727B', '#FE8463', '#9BCA63', '#FAD860', '#F3A43B', '#60C0DD', '#D7504B', '#C6E579', '#F4E001', '#F0805A', '#26C0C0'];
                                    return colorList[params.dataIndex]
                                }
                            }
                        }
                    }
                ]
            };
            top_10_industry_further.setOption(option);
            top_10_industry_further.hideLoading();
            var option2 = {
                title : {
                    text: data['title'] + "行业磁盘类型分布",
                    //subtext: '纯属虚构',
                    x: 'left',
                    textStyle: {
                        fontSize: 10
                    }
                },
                tooltip : {
                    trigger: 'item',
                    formatter: "{a} <br/>{b} : {c} ({d}%)"
                },
                legend: {
                    orient: 'vertical',
                    x: 'left',
                    y: 'bottom',
                    data: data['data4']
                },
                series : [
                    {
                        name: '磁盘类型',
                        type: 'pie',
                        //radius : '55%',
                        //center: ['50%', '60%'],
                        data: data['data5'],
                        itemStyle: {
                            emphasis: {
                                shadowBlur: 10,
                                shadowOffsetX: 0,
                                shadowColor: 'rgba(0, 0, 0, 0.5)'
                            }
                        }
                    }
                ]
            };
            top_10_industry_further2.setOption(option2);
            top_10_industry_further2.hideLoading();
        });
    }
});

// 公司前十模态
top_10_company.on('click', function (params) {
    // 控制台打印数据的名称
    console.log(params);
    if (params.data.selected) {
        modal_company.show();
        // 记录公司名字到button里面备用
        var company_name = $(".modal-time").attr('company', params.name);
        console.log(company_name);
        // new
        var top_10_company_further = echarts.init(document.getElementById('top_10_company_further'));
        var top_10_company_further2 = echarts.init(document.getElementById('top_10_company_further2'));

        // loading
        top_10_company_further.showLoading();
        top_10_company_further2.showLoading();

        // run
        // 需要把定义好的echarts传进去
        get_instance_pure_increase_company({name: 'month', company_name: params.name });
        $.get('/top_10_company_count_further/', {CompanyName: params.name}).done(function (data) {
            var option = {
                title: {
                    text: data['title'] + "DB类型与版本分布",
                    //subtext: '纯属虚构',
                    x: 'left',
                    textStyle: {
                        fontSize: 10
                    }
                },
                tooltip: {
                    trigger: 'item',
                    formatter: "{a} <br/>{b}: {c} ({d}%)"
                },
                legend: {
                    orient: 'vertical',
                    x: 'right',
                    y: 'bottom',
                    data: data['category']
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
                        radius: ['45%', '60%'],

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
                        radius: ['65%', '75%'],

                        data: data['data3'],
                        itemStyle: {
                            normal: {
                                color: function (params) {
                                    // 构建自己想要的颜色库
                                    var colorList = ['#C1232B', '#B5C334', '#FCCE10', '#E87C25', '#27727B', '#FE8463', '#9BCA63', '#FAD860', '#F3A43B', '#60C0DD', '#D7504B', '#C6E579', '#F4E001', '#F0805A', '#26C0C0'];
                                    return colorList[params.dataIndex]
                                }
                            }
                        }
                    }
                ]
            };
            top_10_company_further.setOption(option);
            top_10_company_further.hideLoading();
            var option2 = {
                title : {
                    text: data['title'] + "磁盘类型分布",
                    //subtext: '纯属虚构',
                    x: 'left',
                    textStyle: {
                        fontSize: 10
                    }
                },
                tooltip : {
                    trigger: 'item',
                    formatter: "{a} <br/>{b} : {c} ({d}%)"
                },
                legend: {
                    orient: 'vertical',
                    x: 'left',
                    y: 'bottom',
                    data: data['data4']
                },
                series : [
                    {
                        name: '磁盘类型',
                        type: 'pie',
                        //radius : '55%',
                        //center: ['50%', '60%'],
                        data: data['data5'],
                        itemStyle: {
                            emphasis: {
                                shadowBlur: 10,
                                shadowOffsetX: 0,
                                shadowColor: 'rgba(0, 0, 0, 0.5)'
                            }
                        }
                    }
                ]
            };
            top_10_company_further2.setOption(option2);
            top_10_company_further2.hideLoading();
        });
    }
});

// 中间方法
function middle_fuc(button) {
    console.log(button);
    var middle_json = {
        name: button.name,
        company_name: $(button).attr('company')
    };
    console.log(middle_json);
    get_instance_pure_increase_company(middle_json)
}
//
function get_instance_pure_increase_company(json_data) {
    console.log(json_data);
    var instance_pure_increase_company = echarts.init(document.getElementById('instance_pure_increase_company'));
    instance_pure_increase_company.showLoading();
    $.get('/instance_pure_increase_by_company/', {'time_grading': json_data.name, 'company_name': json_data.company_name}).done(function (data) {
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
                //selected: {
                //    '净增': true
                //}
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
                    name:'申请',
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
            ],
            grid: {
                left: '8%',
                right: '8%',
                bottom: '3%',
                containLabel: false
            }
        };

        instance_pure_increase_company.hideLoading();
        instance_pure_increase_company.setOption(option);
    });
}