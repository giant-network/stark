import React, { Fragment } from 'react';
import { Layout, Icon } from 'antd';
import GlobalFooter from '@/components/GlobalFooter';

const { Footer } = Layout;
const FooterView = () => (
  <Footer style={{ padding: 0 }}>
    <GlobalFooter
      links={[
        {
          key: '谷歌',
          title: '谷歌搜索',
          href: 'https://www.google.com',
          blankTarget: true,
        },
        {
          key: 'github',
          title: <Icon type="github" />,
          href: 'https://github.com',
          blankTarget: true,
        },
        {
          key: 'Stack',
          title: 'Stack Overflow',
          href: 'https://stackoverflow.com',
          blankTarget: true,
        },
      ]}
      copyright={
        <Fragment>
          Copyright <Icon type="copyright" /> 元气满满部出品
        </Fragment>
      }
    />
  </Footer>
);
export default FooterView;
