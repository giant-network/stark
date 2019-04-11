import React, { Fragment } from 'react';
import { Layout, Icon } from 'antd';
import GlobalFooter from '@/components/GlobalFooter';

const { Footer } = Layout;
const FooterView = () => (
  <Footer style={{ padding: 0 }}>
    <GlobalFooter
      links={[
        {
          key: '巨人网络',
          title: '巨人网络',
          href: 'http://www.ztgame.com/',
          blankTarget: true,
        },
        {
          key: 'github',
          title: <Icon type="github" />,
          href: 'https://github.com/ant-design/ant-design-pro',
          blankTarget: true,
        },
        {
          key: '加入巨人',
          title: '加入巨人',
          href: 'http://hr.ztgame.com/',
          blankTarget: true,
        },
      ]}
      copyright={
        <Fragment>
          Copyright <Icon type="copyright" /> 2019 巨人网络技术保障部出品
        </Fragment>
      }
    />
  </Footer>
);
export default FooterView;
