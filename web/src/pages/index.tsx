import React, { useState } from 'react';
import './index.less';
import { Popconfirm, Table, Form, Input, Button, Checkbox, Modal, Card, PageHeader, Tag, Statistic, Row, message, Divider, Col } from 'antd';
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
      RefreshClusterStatus('manage', 'noTitleKey')
    }
  )

  // Tables
  const columns = [
    { title: 'Kubernetes Nodes', dataIndex: 'node', key: 'node' },
    { title: 'Namespace', dataIndex: 'namespace', key: 'namespace' },
    { title: 'Status', dataIndex: 'status', key: 'status' },
    {
      title: 'Action',
      dataIndex: 'x',
      key: 'node',
      render: (_, record) => <div>
        <Popconfirm
          title="Are you sure you want to delete it?"
          onConfirm={(event) => {
            request.post('/api/delete', {
              method: 'POST',
              data: { 'apiserver': record.node, 'namespace': record.namespace }
            }).then(function (response) {
              message.success('Delete Proposal Submitted')
              RefreshClusterStatus('manage', 'noTitleKey')
            })
              .catch(function (error) {
                console.log(error);
              });
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
    request('/api/deploy', {
      method: 'POST',
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
        message.success("Proposal Submitted. Wait for Cluster Ready")
      })
      .catch(function (error) {
        message.error(error.data)
      });
    RefreshClusterStatus('manage', 'noTitleKey')
  };

  const onFinishFailed = errorInfo => {
    console.log('Failed:', errorInfo);
  };

  const contentListNoTitle = {
    manage: <div>
      <Table
        columns={columns}
        dataSource={pageState.servertables}
      />
    </div>,
    recharge: <div>
    </div>,
  };


  const RefreshClusterStatus = (key, type) => {
    if (key === 'manage') {
      request.get('/api/status')
        .then(function (response) {
          setPageState({
            ...pageState,
            [type]: key,
            servertables: response
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
        subTitle=""
        extra={[
          <Button key="2" onClick={showModal} type="primary">Deploy</Button>,
        ]}
      >
        <Modal
          title="Deployment"
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
            initialValues={{
              apiserver: '',
              api_token: '',
              namespace: '',
              pd_version: '3.0.13',
              tikv_version: '3.0.13',
              tidb_version: '3.0.13',
              pd_replicates: 3,
              tikv_replicates: 3,
              tidb_replicates: 2
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
                  <TextArea rows={4} />
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

          </Form>
        </Modal>
      </PageHeader>
      <br />
      <Card
        style={{ width: '100%' }}
        tabList={tabListNoTitle}
        activeTabKey={pageState.noTitleKey}
        RefreshClusterStatus={key => {
          RefreshClusterStatus(key, 'noTitleKey');
        }}
      >
        {contentListNoTitle[pageState.noTitleKey]}
      </Card>
    </div>
  )
};
