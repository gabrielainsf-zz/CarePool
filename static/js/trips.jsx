/* start class */

class TripDisplay extends React.Component {
    constructor(props) {
        super(props)
         this.state = {
            Origin: ''
            Destination: ''
            Date: ''

        };
    }

  componentDidMount() {
    // When the component has been rendered, attempt to update this.state
    this.updateTrips();
  }

    // Since this will be a callback function, we write it as an arrow function
  updateTrips = () => {
    fetch(this.props.route)
      .then(res => res.json())
      .then(data => {
        // Clean up trips data

        #### TO DO####
        ## loop through trips
        ## key into each info and set to variable 
        const origin = data.forecast;
        const destination = 
        const date =

        rawForecast[0].toLowerCase() + rawForecast.slice(1);

        this.setState({ forecast: `The weather will be ${cleanForecast}` });
      })
      // Handle errors if the request fails
      .catch(err => this.setState({ forecast: 'Something went wrong!' }));
  }

    render() {
    return (
      <div className="TripDisplay">
        < text={this.state.forecast} />
      </div>
    );
  }

}

/* end class */