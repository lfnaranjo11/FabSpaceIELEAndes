import axios from 'axios';

const instance = axios.create({
  // baseURL: 'http://LoadBalancerDespC-125555267.us-east-1.elb.amazonaws.com:8000/api/',
  //baseURL: 'http://LoadBalancerDespC-125555267.us-east-1.elb.amazonaws.com/api',
  //baseURL: 'https://jsonplaceholder.typicode.com/',
  baseURL: `http://${process.env.REACT_APP_BACK_END}/restapi/`,
  responseType: 'json',
});

export default instance;
