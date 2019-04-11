import React, { PureComponent } from 'react';
import { connect } from 'dva';
import { Card, Button, Icon, List } from 'antd';

import Ellipsis from '@/components/Ellipsis';
import PageHeaderWrapper from '@/components/PageHeaderWrapper';
import styles from './styles/HomePage.less';
import cookie from 'react-cookies'

@connect(({ list, loading }) => ({
  list,
  loading: loading.models.list,
}))
class CardList extends PureComponent {
    constructor(props) {
      super(props);
      let cookieCard = cookie.load('cardId');
      let loadCookieCard = Array.isArray(cookieCard) ? cookieCard : [];
      this.state = {
        isShow: "common",
        search: false,
        collectedCard: loadCookieCard,
      };

    };

  fetchData = (id) => {
    if (id === '0') {
        this.props.dispatch({
          type: 'list/fetchCollectedCardsList',
          payload: {
            ids: JSON.stringify(this.state.collectedCard),
          },
        });
    }  else {
        this.props.dispatch({
          type: 'list/fetch',
          payload: {
            id: id,
          },
        });
    }
  };

  componentDidUpdate(prevProps, prevState) {
      const {list: { cardsList }} = this.props;
      if (cardsList.name === 'searchCard') {
          this.setState({isShow: 'common', search: true})
      }else {
          this.setState({search: false})
      }
  }

  componentDidMount() {
    const { dispatch } = this.props;
    dispatch({
      type: 'list/fetchTabs',
    }).then(
      () => {
        const {list: { tabsList }} = this.props;
        tabsList.unshift({id: '0', name: "我的收藏 ☆"});
        this.setState({isShow: tabsList[0].id.toString()});
        this.fetchData(tabsList[0].id);
      }
    );
  }

  handleTabChange = id => {
    this.setState({ isShow: id}, () => this.fetchData(id));
  };

  collectClick = (key) => {
      let collectCard = this.state.collectedCard;
      const keyIndex = collectCard.indexOf(key);
      if (keyIndex < 0) {
          collectCard.push(key);
          cookie.save('cardId', collectCard, { path: '/' });
      }else {
          collectCard.splice(keyIndex, 1);
          cookie.save('cardId', collectCard, { path: '/' });
      }
      this.setState({collectedCard: collectCard});
      this.props.dispatch({
          type: 'list/reloadCards',
          payload: this.props.list.cardsList
      });
  };

  render() {
    const {list: { cardsList, tabsList }, loading} = this.props;

    const content = (
      <div className={styles.pageHeaderContent}>
        <p>
          Stark 集合了巨人所有站点的入口，提供一站式的便捷访问，快试试把他设为你的主页吧。
        </p>
      </div>
    );

    const { match, children, location } = this.props;
    const cards = cardsList.cards;
    cards.sort((a, b) => {
      return b.weight - a.weight;
    });

    return (
      <PageHeaderWrapper title="Stark" content={content} hiddenBreadcrumb={true}
                         tabList={tabsList}
                         tabActiveKey={this.state.isShow}
                         onTabChange={this.handleTabChange}>
        <div className={styles.cardList}>
          {this.state.search ? <p style={{textAlign: 'center', marginBottom: 15, color: '#2196f3'}}>为您找到相关结果 {cards.length} 个</p>: ''}
          <List
            rowKey="id"
            loading={loading}
            grid={{ gutter: 18, lg: 4, md: 3, sm: 1, xs: 1 }}
            dataSource={cards}
            renderItem={item =>
              item ?
                (<List.Item key={item.id}>
                  <Card className={styles.card} actions={item.menus.map((value, key) => <a key={key} href={value.link} target="_blank">{value.name}</a>)}>
                    <Card.Meta
                      avatar={<img alt="" className={styles.cardAvatar} src={item.avatar} />}
                      title= {this.state.collectedCard.indexOf(item.id) > -1 ?
                          <span>{item.name} <a className={styles.cardCollected} onClick={this.collectClick.bind(this, item.id)} title={"取消收藏"}>★</a></span> :
                          <span>{item.name} <a className={styles.cardCollect} onClick={this.collectClick.bind(this, item.id)} title={"点击收藏"}>☆</a></span>}
                      description={
                        <Ellipsis className={styles.item} lines={3} tooltip={true}>
                          {item.description}
                        </Ellipsis>
                      }
                    />
                  </Card>
                </List.Item>)
             : (<span/>)
            }
          />
        </div>
      </PageHeaderWrapper>
    );
  }
}

export default CardList;
