import React, { Fragment } from 'react';
import { Layout, Icon } from 'antd';
import GlobalFooter from '@/components/GlobalFooter';
import request from '@/utils/request';

const { Footer } = Layout;

class FooterView extends React.Component {
  state = {
    footerConfig: {
      link1: { name: '谷歌搜索', url: 'https://www.google.com/' },
      link2: { name: 'ChatGPT', url: 'https://chatgpt.com/' },
      copyright: '元气满满部出品'
    }
  };

  componentDidMount() {
    // 从后端获取页脚配置
    this.fetchFooterConfig();
  }

  fetchFooterConfig = async () => {
    try {
      const response = await request('/api/config/footer/');
      if (response) {
        this.setState({ footerConfig: response });
      }
    } catch (error) {
      console.error('获取页脚配置失败，使用默认配置', error);
    }
  };

  render() {
    const { footerConfig } = this.state;

    return (
      <Footer style={{ padding: 0 }}>
        <GlobalFooter
          links={[
            {
              key: 'link1',
              title: footerConfig.link1.name,
              href: footerConfig.link1.url,
              blankTarget: true,
            },
            {
              key: 'github',
              title: <Icon type="github" />,
              href: 'https://github.com',
              blankTarget: true,
            },
            {
              key: 'link2',
              title: footerConfig.link2.name,
              href: footerConfig.link2.url,
              blankTarget: true,
            },
          ]}
          copyright={
            <Fragment>
              Copyright <Icon type="copyright" /> {footerConfig.copyright}
            </Fragment>
          }
        />
      </Footer>
    );
  }
}

export default FooterView;
