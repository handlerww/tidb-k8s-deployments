import React, { useState } from 'react';
import './index.less';
import { Popconfirm, Table, Form, Input, Button, Checkbox, Modal,Card, PageHeader, Tag, Statistic, Row, message, Divider, Col } from 'antd';
import { useMount } from '@umijs/hooks';
import request from 'umi-request';

const { TextArea } = Input;

export default () => {

  const [pageState, setPageState] = useState({
    noTitleKey: 'manage',
    balance: 0,
    servers: 0,
    servertables: [],
    visible: false,
    confirmLoading: false,
  });


  useMount(
    () => {
      onTabChange('manage','noTitleKey')
    }
  )
  
  // Tables
  const columns = [
    { title: 'Nodes', dataIndex: 'ip', key: 'ip' },
    { title: 'Status', dataIndex: 'map', key: 'map' },
    {
      title: 'Action',
      dataIndex: '',
      key: 'x',
      render: () => <div>
        <Popconfirm
          title="Are you sure you want to delete it?"
          onConfirm={(event) => {
            console.log(event)
            // request.post('http://127.0.0.1:5000/delete', {
            //   method: 'POST',
            //   data: { 'username': 'ioaejr' }
            // }).then(function (response) {
            //   setPageState({
            //     ...pageState,
            //     servertables: response['servers'],
            //   });
            // })
            //   .catch(function (error) {
            //     console.log(error);
            //   });
          }}
          onCancel={() => {
          }}
          okText="Yes"
          cancelText="No"
        >
          <a href="#">Delete</a>
        </Popconfirm>
      </div>,
    },
  ];

  const tabListNoTitle = [
    {
      key: 'manage',
      tab: 'Cluster',
    },
  ];

  const onFinish = values => {
    request.post('http://127.0.0.1:5000/deploy', {
      method: 'POST',
      data: values
    }).then(function (response) {
      console.log(response)
    })
      .catch(function (error) {
        console.log(error);
      });

    request.put('http://rap2.taobao.org:38080/app/mock/232687/servers/create', {
      method: 'PUT',
      data: values
    })
      .then(function (response) {
        console.log(values)
        setPageState({
          ...pageState,
          confirmLoading: true,
        });
        setTimeout(() => {
          setPageState({
            ...pageState,
            visible: false,
            confirmLoading: false,
          });
        }, 1000);
        message.success("成功创建,服务器信息请看管理页面")
      })
      .catch(function (error) {
        console.log(error);
      });
  };

  const onFinishFailed = errorInfo => {
    console.log('Failed:', errorInfo);
  };

  const contentListNoTitle = {
    create: <div>
      
    </div>,
    manage: <div>
      <Table
        columns={columns}
        dataSource={pageState.servertables}
      />
    </div>,
    recharge: <div>
    </div>,
  };


  const onTabChange = (key, type) => {
    if (key === 'manage') {
      request.get('http://rap2.taobao.org:38080/app/mock/232687/servers/status')
        .then(function (response) {
          setPageState({
            ...pageState,
            [type]: key,
            servertables: response['result']
          });
        })
        .catch(function (error) {
          console.log(error);
        });

    } else {
      setPageState({
        ...pageState,
        [type]: key
      });
    }

  };

  // if (loading) {
  //   return <Skeleton active />
  // }
  const showModal = () => {
    setPageState({
      ...pageState,
      visible: true,
    });
  };

  const handleOk = () => {
    
  };

  const handleCancel = () => {
    setPageState({
      ...pageState,
      visible: false,
    });
  };
  const [form] = Form.useForm();

  return (
    <div className="site-page-header-ghost-wrapper" >
      <PageHeader
        ghost={false}
        onBack={() => window.history.back()}
        title="TiDB Cluster Manager"
        tags={<Tag color="blue">1 Cluster is Running</Tag>}
        subTitle=""
        extra={[
          <Button key="2" onClick={showModal} type="primary">Deploy</Button>,
        ]}
      >
        <Modal
          title="Title"
          width={800}
          visible={pageState.visible}
          onOk={() => {
            form
              .validateFields()
              .then(values => {
                form.resetFields();
                onFinish(values);
              })
              .catch(info => {
                console.log('Validate Failed:', info);
              });
          }}
          confirmLoading={pageState.confirmLoading}
          onCancel={handleCancel}
        >
          <Form
        name="basic"
        form={form}
        initialValues={{ monitor: true,
          apiserver:'https://47.113.195.245:6443',
          api_token:'eyJhbGciOiJSUzI1NiIsImtpZCI6IkZack1lcjY5SzRkc0UxaTUtZE00S0lqNWpEZnRDVUpjMEFZZ0M2TEZ2TUkifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJhZG1pbi11c2VyLXRva2VuLW1neG1qIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6ImFkbWluLXVzZXIiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC51aWQiOiJmNmYwN2NlZS0xOTJmLTQ3YmMtOWRhNi1lZmQxMDQzYWY1YzkiLCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6a3ViZS1zeXN0ZW06YWRtaW4tdXNlciJ9.Xo4RpuG2LuOCchgsAKxMGHIljDt5zl-fpxcZiFnCexVmnF4vtEjXqGXVb-BoZf9UbYbhmiQlh9iuL1ImURUYrPFoZXGyxsOZZmlXkJZIsiB8JAsc2vtM5CB7ESsG1-T6DltxngtwTIlsJ9Zqvo9YF288Hj1oVUsz9Oq0lCT8DFR_4NJ3lK-K8s7Iv12amz87Y2PnlGpVRoW3d9Xxy0SS76B3S5x3PMUZau_FhzqqE-LJXnHjUSBm39zeZ6EXeIbd17EaO_j9mN40UoYhV7LOKwj_2xql7ojsAVXJBdy77FPWQAPjvR5hGmQc83VmORZcX7-MxNrUGJwrLIkr7940oA',
          namespace:'try',
          pd_version:'3.0.13',
          tikv_version:'3.0.13',
          tidb_version:'3.0.13',
          pd_replicates:3,
          tikv_replicates:3,
          tidb_replicates:2
        }}
      >
        <Divider orientation="left" style={{ color: '#333', fontWeight: 'normal' }}>
          Cluster Info
      </Divider>
        <Row gutter={16}>
        <Col className="gutter-row" span={12}>
            <Form.Item
              label="APIServer"
              name="apiserver"
            >
              <Input />
            </Form.Item>
          </Col>
          <Col className="gutter-row" span={12}>
            <Form.Item
              label="Namespace"
              name="namespace"
            >
              <Input />
            </Form.Item>
          </Col>
          <Col className="gutter-row" span={24}>
            <Form.Item
              label="API Token"
              name="api_token"
            >
              <TextArea  rows={4}/>
            </Form.Item>
          </Col>
        </Row>
        <Divider orientation="left" style={{ color: '#333', fontWeight: 'normal' }}>
          Version
      </Divider>
        <Row gutter={16}>
          <Col className="gutter-row" span={8}>
            <Form.Item
              label="PD Version"
              name="pd_version"
            >
              <Input />
            </Form.Item>
          </Col>
          <Col className="gutter-row" span={8}>
            <Form.Item
              label="TiKV Version"
              name="tikv_version"
            >
              <Input />
            </Form.Item>
          </Col>
          <Col className="gutter-row" span={8}>
            <Form.Item
              label="TiDB Version"
              name="tidb_version"
            >
              <Input />
            </Form.Item>
          </Col>
        </Row>
        <Divider orientation="left" style={{ color: '#333', fontWeight: 'normal' }}>
          Replicates
      </Divider>
        <Row gutter={16}>
          <Col className="gutter-row" span={8}>
            <Form.Item
              label="PD replicates"
              name="pd_replicates"
            >
              <Input />
            </Form.Item>
          </Col>
          <Col className="gutter-row" span={8}>
            <Form.Item
              label="TiKV replicates"
              name="tikv_replicates"
            >
              <Input />
            </Form.Item>
          </Col>
          <Col className="gutter-row" span={8}>
            <Form.Item
              label="TiDB replicates"
              name="tidb_replicates"
            >
              <Input />
            </Form.Item>
          </Col>
        </Row>


        <Form.Item name="monitor" valuePropName="checked">
          <Checkbox>Monitor?</Checkbox>
        </Form.Item>

        
      </Form>
        </Modal>
      </PageHeader>
      <br />
      <Card
        style={{ width: '100%' }}
        tabList={tabListNoTitle}
        activeTabKey={pageState.noTitleKey}
        onTabChange={key => {
          onTabChange(key, 'noTitleKey');
        }}
      >
        {contentListNoTitle[pageState.noTitleKey]}
      </Card>
    </div>
  )
};
