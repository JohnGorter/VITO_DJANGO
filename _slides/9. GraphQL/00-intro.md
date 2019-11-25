# GRAPHQL

---
### GRAPHQL

> GraphQL is a query language for your API, and a server-side runtime for executing queries by using a type system you define for your data.

http://graphql.org


---
### GRAPHQL (2)

<img src="/images/gq1.png" />

---
### GRAPHQL 

GraphQL is not a library, but a language spec.

<img src="/images/gq2.png" />

---
### GRAPHQL 

GraphQL schema defines the structure of valid queries and the return data types of them. It's the protocol the client & server use to communicate under.

<img src="/images/gq3.png" />

---
### GRAPHQL 

Some queries allow to pass in arguments. The schema defines all valid arguments
On the backend, we need to have resolvers

<img src="/images/gq4.png" />

---
### GRAPHQL 

When we select the same field multiple times, each time with a different argument (like in the pic). This will cause naming conflicts, so we need aliases

<img src="/images/gq5.png" />


---
### GRAPHQL 

We can wrap "subfields" into a Fragment and reuse them with the spread operator in selections. Useful when we select the same fields over and over again.

<img src="/images/gq6.png" />

---
### GRAPHQL 

Using GraphQL variables makes it easy to modularize and share/reuse our prewritten query code. We declare them at the beginning of a query, and are allowed to assign default values to them.

<img src="/images/gq7.png" />

---
### GRAPHQL 

Interfaces allow to flexibly create complex data types in an OOP manner.

When the return type is an interface, the on keyword is for conditionally access fields of a specific implementation.

<img src="/images/gq8.png" />

---
### GRAPHQL 

Contrary to queries, a Mutation operation is used to change the serverside data - eg. to create an account, generate auth token, or add data entries.

<img src="/images/gq9.png" />

---
### GRAPHQL 

Instead of sending queries over HTTP back and forth, GraphQL also has a Subscription operation type for creating WebSocket connections, so the server can push continuous updates to the client

<img src="/images/gq10.png" />

---
### GRAPHQL vs REST


---
<!-- .slide: data-background="url('images/demo.jpg')" data-background-size="cover" --> 
<!-- .slide: class="lab" -->
## Demo time!
Creating a GraphQl server in NodeJS





