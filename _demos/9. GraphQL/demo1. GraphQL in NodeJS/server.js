// // demo 1

// var express = require('express');
// var GraphqlHTTP = require('express-graphql');
// var { buildSchema } = require('graphql');

// var schema = buildSchema(`
//     type Query { 
//         hello: User
//     }

//     type User {
//         id:Int
//         name:String
//     }
// `);



// var root = { hello: function () { return { id:10, name:"john gorter"}; }};

// var app = express(); 
// app.use('/graphql', GraphqlHTTP({
//     schema:schema,
//     rootValue: root, 
//     graphiql: true
// }));
// app.listen(4000, () => console.log('server running'));



// demo2
//
let { GraphQLServer } = require('graphql-yoga');

let links = [{
    id: 'link-0',
    url: 'www.howtographql.com',
    description: 'Fullstack tutorial for GraphQL'
  }]
  // 1
let idCount = links.length
const resolvers = {
    Query: {
        info: () => `This is the API of a Hackernews Clone`,
        feed: () => links,
    },
    Mutation: {
        // 2
        test: (p, a) =>{
            console.log(p, a);
            return links[0];
        },
        post: (parent, args) => {
            const link = {
            id: `link-${idCount++}`,
            description: args.description,
            url: args.url,
        }
        links.push(link)
        return link
        }
    },
}


const typeDefs = `
type Query {
  info: String!
  feed: [Link!]!
}

type Mutation {
  post(url: String!, description: String!): Link!
  test(url: String!): Link!
}

type Link {
  id: ID!
  description: String!
  url: String!
}`;

const server = new GraphQLServer({
    typeDefs: typeDefs,
    resolvers,
    graphiql: true
  })

server.start(() => console.log(`Server is running on http://localhost:4000`))