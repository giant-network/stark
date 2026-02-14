import React, { PureComponent } from 'react';
import { connect } from 'dva';
import { Card, Button, Icon, List, message } from 'antd';

import Ellipsis from '@/components/Ellipsis';
import PageHeaderWrapper from '@/components/PageHeaderWrapper';
import styles from './styles/HomePage.less';
import cookie from 'react-cookies';

@connect(({ list, loading }) => ({
  list,
  loading: loading.models.list,
}))
class CardList extends PureComponent {
  constructor(props) {
    super(props);
    
    // 优化：使用 localStorage 替代 cookie，数据持久化
    let storedCard = localStorage.getItem('stark_favorite_cards');
    let loadCookieCard = storedCard ? JSON.parse(storedCard) : [];
    
    this.state = {
      isShow: 'common',
      search: false,
      collectedCard: loadCookieCard,
      siteTitle: 'Stark', // 默认值
      siteDescription: 'Stark 集合了众多站点的入口，提供一站式的便捷访问，快试试把他设为你的主页吧。', // 默认值
    };
  }

  fetchData = id => {
    if (id === '0') {
      this.props.dispatch({
        type: 'list/fetchCollectedCardsList',
        payload: {
          ids: JSON.stringify(this.state.collectedCard),
        },
      });
    } else {
      this.props.dispatch({
        type: 'list/fetch',
        payload: {
          id: id,
        },
      });
    }
  };

  componentDidUpdate(prevProps, prevState) {
    const {
      list: { cardsList },
    } = this.props;
    if (cardsList.name === 'searchCard') {
      this.setState({ isShow: 'common', search: true });
    } else {
      this.setState({ search: false });
    }
  }

  componentDidMount() {
    // 数据迁移：从旧的 cookie 迁移到 localStorage（只执行一次）
    this.migrateFromCookie();
    
    // 获取网站配置（导航语）
    this.fetchSiteConfig();
    
    const { dispatch } = this.props;
    dispatch({
      type: 'list/fetchTabs',
    }).then(() => {
      const {
        list: { tabsList },
      } = this.props;
      
      // 动态调整"我的收藏"位置：有收藏放第一个，没有收藏放最后
      const favoriteTab = { id: '0', name: '我的收藏 ☆', weight: 999999 };
      let defaultTabId;
      
      if (this.state.collectedCard.length > 0) {
        // 有收藏，放在第一个
        tabsList.unshift(favoriteTab);
        defaultTabId = '0';
      } else {
        // 没有收藏，放在最后
        tabsList.push(favoriteTab);
        defaultTabId = tabsList[0].id.toString();
      }
      
      this.setState({ isShow: defaultTabId });
      this.fetchData(defaultTabId);
    });
  }

  // 获取网站配置
  fetchSiteConfig = () => {
    fetch('/api/config/site/')
      .then(response => response.json())
      .then(data => {
        this.setState({
          siteTitle: data.title || 'Stark',
          siteDescription: data.description || 'Stark 集合了众多站点的入口，提供一站式的便捷访问，快试试把他设为你的主页吧。'
        });
      })
      .catch(error => {
        console.error('获取网站配置失败:', error);
        // 使用默认值，已在 state 中设置
      });
  };

  // 数据迁移：从 cookie 迁移到 localStorage
  migrateFromCookie = () => {
    try {
      const oldCookieData = cookie.load('cardId');
      const existingData = localStorage.getItem('stark_favorite_cards');
      
      if (oldCookieData && Array.isArray(oldCookieData) && !existingData) {
        localStorage.setItem('stark_favorite_cards', JSON.stringify(oldCookieData));
        cookie.remove('cardId', { path: '/' });
      }
    } catch (error) {
      console.error('数据迁移失败:', error);
    }
  };

  handleTabChange = id => {
    this.setState({ isShow: id }, () => this.fetchData(id));
  };

  collectClick = key => {
    const { collectedCard } = this.state;
    const keyIndex = collectedCard.indexOf(key);
    
    // 使用不可变数据更新
    let newCollectedCard;
    const isCollecting = keyIndex < 0;
    
    if (isCollecting) {
      newCollectedCard = [...collectedCard, key];
    } else {
      newCollectedCard = collectedCard.filter((_, index) => index !== keyIndex);
    }
    
    // 保存到 localStorage
    try {
      localStorage.setItem('stark_favorite_cards', JSON.stringify(newCollectedCard));
      // 显示操作反馈
      message.success(isCollecting ? '收藏成功' : '已取消收藏');
    } catch (error) {
      console.error('保存收藏失败:', error);
      message.error('操作失败，请重试');
    }
    
    this.setState({ collectedCard: newCollectedCard });
    
    // 动态调整标签位置：从无到有或从有到无时重新排列标签
    const hadFavorites = collectedCard.length > 0;
    const hasFavorites = newCollectedCard.length > 0;
    
    if (hadFavorites !== hasFavorites) {
      // 收藏状态发生变化（0->1 或 n->0），重新调整标签顺序
      this.adjustFavoriteTabPosition(hasFavorites);
    }
    
    this.props.dispatch({
      type: 'list/reloadCards',
      payload: this.props.list.cardsList,
    });
  };

  // 动态调整"我的收藏"标签位置
  adjustFavoriteTabPosition = (hasFavorites) => {
    const { list: { tabsList } } = this.props;
    
    // 移除现有的"我的收藏"标签
    const favoriteIndex = tabsList.findIndex(tab => tab.id === '0');
    if (favoriteIndex > -1) {
      tabsList.splice(favoriteIndex, 1);
    }
    
    // 根据是否有收藏重新插入
    const favoriteTab = { id: '0', name: '我的收藏 ☆', weight: 999999 };
    if (hasFavorites) {
      // 有收藏，放在第一个
      tabsList.unshift(favoriteTab);
    } else {
      // 没有收藏，放在最后
      tabsList.push(favoriteTab);
    }
    
    // 强制更新以重新渲染标签
    this.forceUpdate();
  };

  render() {
    const {
      list: { cardsList, tabsList },
      loading,
    } = this.props;

    const content = (
      <div className={styles.pageHeaderContent}>
        <p>{this.state.siteDescription}</p>
      </div>
    );

    // 安全地处理 cards 数组并排序
    const cards = cardsList?.cards || [];
    const sortedCards = [...cards].sort((a, b) => b.weight - a.weight);

    return (
      <PageHeaderWrapper
        title={this.state.siteTitle}
        content={content}
        hiddenBreadcrumb={true}
        tabList={tabsList}
        tabActiveKey={this.state.isShow}
        onTabChange={this.handleTabChange}
      >
        <div className={styles.cardList}>
          {this.state.search ? (
            <p style={{ textAlign: 'center', marginBottom: 15, color: '#2196f3' }}>
              为您找到相关结果 {sortedCards.length} 个
            </p>
          ) : (
            ''
          )}
          <List
            rowKey="id"
            loading={loading}
            grid={{ gutter: 18, lg: 4, md: 3, sm: 1, xs: 1 }}
            dataSource={sortedCards}
            renderItem={item =>
              item ? (
                <List.Item key={item.id}>
                  <Card
                    className={styles.card}
                    actions={item.menus.map((value, key) => (
                      <a key={key} href={value.link} target="_blank" rel="noopener noreferrer">
                        {value.name}
                      </a>
                    ))}
                  >
                    <Card.Meta
                      avatar={<img alt={`${item.name}图标`} className={styles.cardAvatar} src={item.avatar} />}
                      title={
                        this.state.collectedCard.indexOf(item.id) > -1 ? (
                          <span>
                            {item.name}{' '}
                            <a
                              className={styles.cardCollected}
                              onClick={this.collectClick.bind(this, item.id)}
                              title={'取消收藏'}
                            >
                              ★
                            </a>
                          </span>
                        ) : (
                          <span>
                            {item.name}{' '}
                            <a
                              className={styles.cardCollect}
                              onClick={this.collectClick.bind(this, item.id)}
                              title={'点击收藏'}
                            >
                              ☆
                            </a>
                          </span>
                        )
                      }
                      description={
                        <Ellipsis className={styles.item} lines={3} tooltip={true}>
                          {item.description}
                        </Ellipsis>
                      }
                    />
                  </Card>
                </List.Item>
              ) : (
                <span />
              )
            }
          />
        </div>
      </PageHeaderWrapper>
    );
  }
}

export default CardList;
