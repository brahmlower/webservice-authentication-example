import React, { Component } from 'react'
import { CardDeck, Card, Button } from 'react-bootstrap';
import './Dashboard.css';

const BUILDING_1 = {
  name: 'Test Building 1',
  description: 'This is test building 1',
  favorited: false,
  image_url: 'https://cdn.getyourguide.com/img/location_img-2703-1061214306-148.jpg'
}

const BUILDING_2 = {
  name: 'Test Building 2',
  description: 'This is test building 2',
  favorited: false,
  image_url: 'https://www.aecom.com/wp-content/uploads/2015/10/1WTC_Credit-Michael-Mahesh-PANYNJ-810x531.jpg'
}

const BUILDING_3 = {
  name: 'Test Building 3',
  description: 'This is test building 3',
  favorited: false,
  image_url: 'https://www.arch2o.com/wp-content/uploads/2015/07/Arch2O-ShanghaiTower-Gensler-36.jpg'
}

const BUILDING_4 = {
  name: 'Test Building 4',
  description: 'This is test building 4',
  favorited: true,
  image_url: 'https://www.wsp.com/-/media/Project/Asia/Image/bnr-tjctf-1.jpg'
}

const BUILDING_5 = {
  name: 'Test Building 5',
  description: 'This is test building 5',
  favorited: true,
  image_url: 'https://pfnphoto.com/new/wp-content/uploads/2016/08/20150501-shanghai-3725-panorama-1600px.jpg'
}

const BUILDING_6 = {
  name: 'Test Building 6',
  description: 'This is test building 6',
  favorited: true,
  image_url: 'http://images.skyscrapercenter.com/building/tapei101_ext-context_(c)taipeifinancial.jpg'
}

class FavoriteButton extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isFavorite: this.props.isFavorite,
      submit_url: '/buildings/id/favorite'
    };
    this.elem_active = (<i onClick={ this.toggleFavorite } class="fas fa-star favoriteButton" aria-hidden="true"></i>);
    this.elem_inactive = (<i onClick={ this.toggleFavorite } class="far fa-star favoriteButton" aria-hidden="true"></i>);
    this.toggleFavorite = this.toggleFavorite.bind(this);
  }

  toggleFavorite() {
    alert('Item has been toggled. Stubbed');
  }

  render() {
    return (this.state.isFavorite ? this.elem_active : this.elem_inactive);
  }
}

class BuildingCard extends Component {
  constructor(props) {
    super(props);
    this.state = {
      name: this.props.name,
      description: this.props.description,
      favorited: this.props.favorited,
      image_url: this.props.image_url
    };
  }

  render() {
    return (
      <Card className="buildingCard">
        <Card.Img variant="top" src={ this.state.image_url } />
        <Card.Body>
          <Card.Title>
            { this.state.name }
            <FavoriteButton isFavorite={ this.state.favorited } />
          </Card.Title>
          <Card.Text>{ this.state.description }</Card.Text>
        </Card.Body>
      </Card>
    );
  }
}

class Dashboard extends Component {
  constructor(props) {
    super(props);
    this.state = {
      favorites: [BUILDING_4, BUILDING_5, BUILDING_6],
      recently_viewed: [BUILDING_1, BUILDING_2, BUILDING_3, BUILDING_4, BUILDING_5, BUILDING_6],
      errors: []
    };
  }

  render () {
    return (
      <div>
        <div className="dashboardSection">
          <h1>Dashboard</h1>
          <p> Welcome to the account dashboard. From here you can jump to recently viewed building entries, or create and manage new buildings!</p>
          <Button>Create Building</Button>
        </div>

        <div className="dashboardSection">
          <h3>Favorites</h3>
          <CardDeck>
            {this.state.favorites.map( (building, idx) => {
              return (
                <BuildingCard
                  key={ idx }
                  name={ building.name }
                  description={ building.description }
                  favorited={ building.favorited }
                  image_url={ building.image_url }
                />
              )
            })}
          </CardDeck>
        </div>

        <div className="dashboardSection">
          <h3>Recently Viewed</h3>
            <CardDeck className="buildingCardRow">
              {this.state.recently_viewed.map( (building, idx) => {
                return (
                  <BuildingCard
                    key={ idx }
                    name={ building.name }
                    description={ building.description }
                    favorited={ building.favorited }
                    image_url={ building.image_url }
                  />
                )
              })}
            </CardDeck>
        </div>
      </div>
    );
  }
}

export { Dashboard }
