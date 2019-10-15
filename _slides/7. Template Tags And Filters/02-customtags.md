# Custom Template tags 

---
### Custom Template tags 

Write your own template tag
- extend the template engine by defining custom tags
- make them available to your templates using the {% load %} tag

---
### Code layout
The most common place 
- inside a Django app: if they relate to an existing app, it makes sense to bundle them there

- any tags in the conventional location are automatically made available to load within templates
- app should contain a templatetags directory, at the same level as models.py, views.py, etc. 

If this doesn’t already exist, create it 
 - don’t forget the __init__.py file

After adding the templatetags module, you will need to restart your server before you can use the tags or filters in templates.

---
### Example

For example, if your custom tags/filters are in a file called poll_extras.py, your app layout might look like this:
```
polls/
    __init__.py
    models.py
    templatetags/
        __init__.py
        poll_extras.py
    views.py
```

in your template you would use the following:
```
{% load poll_extras %}
```
The app that contains the custom tags must be in INSTALLED_APPS in order for the {% load %} tag to work

---
### Example (2)
To be a valid tag library, the module must contain a module-level variable named register that is a template.Library instance, 

```
from django import template
register = template.Library()
```

Alternatively, template tag modules can be registered through the 'libraries' argument to DjangoTemplates

---
### Writing custom template tags
Tags are more complex than filters, because tags can do anything

Django provides a number of shortcuts that make writing most types of tags easier.

---
### Simple tags
```
django.template.Library.simple_tag()
```
Many template tags take a number of arguments 
– strings 
- template variables 
they return a result after doing some processing based solely on the input arguments and some external information 

For example, a current_time tag might accept a format string and return the time as a string formatted accordingly

To ease the creation of these types of tags, Django provides a helper function, simple_tag

---
### Simple tags (2)
This function, which is a method of django.template.Library, takes a function that accepts any number of arguments, wraps it in a render function and the other necessary bits mentioned above and registers it with the template system.

Our current_time function could be written like this:
```
import datetime
from django import template

register = template.Library()

@register.simple_tag
def current_time(format_string):
    return datetime.datetime.now().strftime(format_string)
```

```
{% current_time "%Y-%m-%d %I:%M %p" as the_time %}
<p>The time is {{ the_time }}.</p>
```

---
### Inclusion tags
Another common type of template tag is the type that displays some data by rendering another template. For example, Django’s admin interface uses custom template tags to display the buttons along the bottom of the “add/change” form pages. Those buttons always look the same, but the link targets change depending on the object being edited – so they’re a perfect case for using a small template that is filled with details from the current object. (In the admin’s case, this is the submit_row tag.)

These sorts of tags are called “inclusion tags”.

Writing inclusion tags is probably best demonstrated by example. Let’s write a tag that outputs a list of choices for a given Poll object, such as was created in the tutorials. We’ll use the tag like this:

{% show_results poll %}
…and the output will be something like this:

<ul>
  <li>First choice</li>
  <li>Second choice</li>
  <li>Third choice</li>
</ul>
First, define the function that takes the argument and produces a dictionary of data for the result. The important point here is we only need to return a dictionary, not anything more complex. This will be used as a template context for the template fragment. Example:

def show_results(poll):
    choices = poll.choice_set.all()
    return {'choices': choices}
Next, create the template used to render the tag’s output. This template is a fixed feature of the tag: the tag writer specifies it, not the template designer. Following our example, the template is very simple:

<ul>
{% for choice in choices %}
    <li> {{ choice }} </li>
{% endfor %}
</ul>
Now, create and register the inclusion tag by calling the inclusion_tag() method on a Library object. Following our example, if the above template is in a file called results.html in a directory  that’s searched by the template loader, we’d register the tag like this:

# Here, register is a django.template.Library instance, as before
@register.inclusion_tag('results.html')
def show_results(poll):
    ...
Alternatively it is possible to register the inclusion tag using a django.template.Template instance:

from django.template.loader import get_template
t = get_template('results.html')
register.inclusion_tag(t)(show_results)
…when first creating the function.

Sometimes, your inclusion tags might require a large number of arguments, making it a pain for template authors to pass in all the arguments and remember their order. To solve this, Django provides a takes_context option for inclusion tags. If you specify takes_context in creating a template tag, the tag will have no required arguments, and the underlying Python function will have one argument – the template context as of when the tag was called.

For example, say you’re writing an inclusion tag that will always be used in a context that contains home_link and home_title variables that point back to the main page. Here’s what the Python function would look like:

@register.inclusion_tag('link.html', takes_context=True)
def jump_link(context):
    return {
        'link': context['home_link'],
        'title': context['home_title'],
    }
Note that the first parameter to the function must be called context.

In that register.inclusion_tag() line, we specified takes_context=True and the name of the template. Here’s what the template link.html might look like:

Jump directly to <a href="{{ link }}">{{ title }}</a>.
Then, any time you want to use that custom tag, load its library and call it without any arguments, like so:

{% jump_link %}
Note that when you’re using takes_context=True, there’s no need to pass arguments to the template tag. It automatically gets access to the context.

The takes_context parameter defaults to False. When it’s set to True, the tag is passed the context object, as in this example. That’s the only difference between this case and the previous inclusion_tag example.

inclusion_tag functions may accept any number of positional or keyword arguments. For example:

@register.inclusion_tag('my_template.html')
def my_tag(a, b, *args, **kwargs):
    warning = kwargs['warning']
    profile = kwargs['profile']
    ...
    return ...
Then in the template any number of arguments, separated by spaces, may be passed to the template tag. Like in Python, the values for keyword arguments are set using the equal sign (“=”) and must be provided after the positional arguments. For example:

{% my_tag 123 "abcd" book.title warning=message|lower profile=user.profile %}
Advanced custom template tags¶
Sometimes the basic features for custom template tag creation aren’t enough. Don’t worry, Django gives you complete access to the internals required to build a template tag from the ground up.

A quick overview¶
The template system works in a two-step process: compiling and rendering. To define a custom template tag, you specify how the compilation works and how the rendering works.

When Django compiles a template, it splits the raw template text into ‘’nodes’‘. Each node is an instance of django.template.Node and has a render() method. A compiled template is, simply, a list of Node objects. When you call render() on a compiled template object, the template calls render() on each Node in its node list, with the given context. The results are all concatenated together to form the output of the template.

Thus, to define a custom template tag, you specify how the raw template tag is converted into a Node (the compilation function), and what the node’s render() method does.

Writing the compilation function¶
For each template tag the template parser encounters, it calls a Python function with the tag contents and the parser object itself. This function is responsible for returning a Node instance based on the contents of the tag.

For example, let’s write a full implementation of our simple template tag, {% current_time %}, that displays the current date/time, formatted according to a parameter given in the tag, in strftime() syntax. It’s a good idea to decide the tag syntax before anything else. In our case, let’s say the tag should be used like this:

<p>The time is {% current_time "%Y-%m-%d %I:%M %p" %}.</p>
The parser for this function should grab the parameter and create a Node object:

from django import template

def do_current_time(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, format_string = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires a single argument" % token.contents.split()[0]
        )
    if not (format_string[0] == format_string[-1] and format_string[0] in ('"', "'")):
        raise template.TemplateSyntaxError(
            "%r tag's argument should be in quotes" % tag_name
        )
    return CurrentTimeNode(format_string[1:-1])
Notes:

parser is the template parser object. We don’t need it in this example.
token.contents is a string of the raw contents of the tag. In our example, it’s 'current_time "%Y-%m-%d %I:%M %p"'.
The token.split_contents() method separates the arguments on spaces while keeping quoted strings together. The more straightforward token.contents.split() wouldn’t be as robust, as it would naively split on all spaces, including those within quoted strings. It’s a good idea to always use token.split_contents().
This function is responsible for raising django.template.TemplateSyntaxError, with helpful messages, for any syntax error.
The TemplateSyntaxError exceptions use the tag_name variable. Don’t hard-code the tag’s name in your error messages, because that couples the tag’s name to your function. token.contents.split()[0] will ‘’always’’ be the name of your tag – even when the tag has no arguments.
The function returns a CurrentTimeNode with everything the node needs to know about this tag. In this case, it just passes the argument – "%Y-%m-%d %I:%M %p". The leading and trailing quotes from the template tag are removed in format_string[1:-1].
The parsing is very low-level. The Django developers have experimented with writing small frameworks on top of this parsing system, using techniques such as EBNF grammars, but those experiments made the template engine too slow. It’s low-level because that’s fastest.
Writing the renderer¶
The second step in writing custom tags is to define a Node subclass that has a render() method.

Continuing the above example, we need to define CurrentTimeNode:

import datetime
from django import template

class CurrentTimeNode(template.Node):
    def __init__(self, format_string):
        self.format_string = format_string

    def render(self, context):
        return datetime.datetime.now().strftime(self.format_string)
Notes:

__init__() gets the format_string from do_current_time(). Always pass any options/parameters/arguments to a Node via its __init__().
The render() method is where the work actually happens.
render() should generally fail silently, particularly in a production environment. In some cases however, particularly if context.template.engine.debug is True, this method may raise an exception to make debugging easier. For example, several core tags raise django.template.TemplateSyntaxError if they receive the wrong number or type of arguments.
Ultimately, this decoupling of compilation and rendering results in an efficient template system, because a template can render multiple contexts without having to be parsed multiple times.

Auto-escaping considerations¶
The output from template tags is not automatically run through the auto-escaping filters (with the exception of simple_tag() as described above). However, there are still a couple of things you should keep in mind when writing a template tag.

If the render() function of your template stores the result in a context variable (rather than returning the result in a string), it should take care to call mark_safe() if appropriate. When the variable is ultimately rendered, it will be affected by the auto-escape setting in effect at the time, so content that should be safe from further escaping needs to be marked as such.

Also, if your template tag creates a new context for performing some sub-rendering, set the auto-escape attribute to the current context’s value. The __init__ method for the Context class takes a parameter called autoescape that you can use for this purpose. For example:

from django.template import Context

def render(self, context):
    # ...
    new_context = Context({'var': obj}, autoescape=context.autoescape)
    # ... Do something with new_context ...
This is not a very common situation, but it’s useful if you’re rendering a template yourself. For example:

def render(self, context):
    t = context.template.engine.get_template('small_fragment.html')
    return t.render(Context({'var': obj}, autoescape=context.autoescape))
If we had neglected to pass in the current context.autoescape value to our new Context in this example, the results would have always been automatically escaped, which may not be the desired behavior if the template tag is used inside a {% autoescape off %} block.

Thread-safety considerations¶
Once a node is parsed, its render method may be called any number of times. Since Django is sometimes run in multi-threaded environments, a single node may be simultaneously rendering with different contexts in response to two separate requests. Therefore, it’s important to make sure your template tags are thread safe.

To make sure your template tags are thread safe, you should never store state information on the node itself. For example, Django provides a builtin cycle template tag that cycles among a list of given strings each time it’s rendered:

{% for o in some_list %}
    <tr class="{% cycle 'row1' 'row2' %}">
        ...
    </tr>
{% endfor %}
A naive implementation of CycleNode might look something like this:

import itertools
from django import template

class CycleNode(template.Node):
    def __init__(self, cyclevars):
        self.cycle_iter = itertools.cycle(cyclevars)

    def render(self, context):
        return next(self.cycle_iter)
But, suppose we have two templates rendering the template snippet from above at the same time:

Thread 1 performs its first loop iteration, CycleNode.render() returns ‘row1’
Thread 2 performs its first loop iteration, CycleNode.render() returns ‘row2’
Thread 1 performs its second loop iteration, CycleNode.render() returns ‘row1’
Thread 2 performs its second loop iteration, CycleNode.render() returns ‘row2’
The CycleNode is iterating, but it’s iterating globally. As far as Thread 1 and Thread 2 are concerned, it’s always returning the same value. This is obviously not what we want!

To address this problem, Django provides a render_context that’s associated with the context of the template that is currently being rendered. The render_context behaves like a Python dictionary, and should be used to store Node state between invocations of the render method.

Let’s refactor our CycleNode implementation to use the render_context:

class CycleNode(template.Node):
    def __init__(self, cyclevars):
        self.cyclevars = cyclevars

    def render(self, context):
        if self not in context.render_context:
            context.render_context[self] = itertools.cycle(self.cyclevars)
        cycle_iter = context.render_context[self]
        return next(cycle_iter)
Note that it’s perfectly safe to store global information that will not change throughout the life of the Node as an attribute. In the case of CycleNode, the cyclevars argument doesn’t change after the Node is instantiated, so we don’t need to put it in the render_context. But state information that is specific to the template that is currently being rendered, like the current iteration of the CycleNode, should be stored in the render_context.

Note

Notice how we used self to scope the CycleNode specific information within the render_context. There may be multiple CycleNodes in a given template, so we need to be careful not to clobber another node’s state information. The easiest way to do this is to always use self as the key into render_context. If you’re keeping track of several state variables, make render_context[self] a dictionary.

Registering the tag¶
Finally, register the tag with your module’s Library instance, as explained in writing custom template filters above. Example:

register.tag('current_time', do_current_time)
The tag() method takes two arguments:

The name of the template tag – a string. If this is left out, the name of the compilation function will be used.
The compilation function – a Python function (not the name of the function as a string).
As with filter registration, it is also possible to use this as a decorator:

@register.tag(name="current_time")
def do_current_time(parser, token):
    ...

@register.tag
def shout(parser, token):
    ...
If you leave off the name argument, as in the second example above, Django will use the function’s name as the tag name.

Passing template variables to the tag¶
Although you can pass any number of arguments to a template tag using token.split_contents(), the arguments are all unpacked as string literals. A little more work is required in order to pass dynamic content (a template variable) to a template tag as an argument.

While the previous examples have formatted the current time into a string and returned the string, suppose you wanted to pass in a DateTimeField from an object and have the template tag format that date-time:

<p>This post was last updated at {% format_time blog_entry.date_updated "%Y-%m-%d %I:%M %p" %}.</p>
Initially, token.split_contents() will return three values:

The tag name format_time.
The string 'blog_entry.date_updated' (without the surrounding quotes).
The formatting string '"%Y-%m-%d %I:%M %p"'. The return value from split_contents() will include the leading and trailing quotes for string literals like this.
Now your tag should begin to look like this:

from django import template

def do_format_time(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, date_to_be_formatted, format_string = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires exactly two arguments" % token.contents.split()[0]
        )
    if not (format_string[0] == format_string[-1] and format_string[0] in ('"', "'")):
        raise template.TemplateSyntaxError(
            "%r tag's argument should be in quotes" % tag_name
        )
    return FormatTimeNode(date_to_be_formatted, format_string[1:-1])
You also have to change the renderer to retrieve the actual contents of the date_updated property of the blog_entry object. This can be accomplished by using the Variable() class in django.template.

To use the Variable class, simply instantiate it with the name of the variable to be resolved, and then call variable.resolve(context). So, for example:

class FormatTimeNode(template.Node):
    def __init__(self, date_to_be_formatted, format_string):
        self.date_to_be_formatted = template.Variable(date_to_be_formatted)
        self.format_string = format_string

    def render(self, context):
        try:
            actual_date = self.date_to_be_formatted.resolve(context)
            return actual_date.strftime(self.format_string)
        except template.VariableDoesNotExist:
            return ''
Variable resolution will throw a VariableDoesNotExist exception if it cannot resolve the string passed to it in the current context of the page.

Setting a variable in the context¶
The above examples simply output a value. Generally, it’s more flexible if your template tags set template variables instead of outputting values. That way, template authors can reuse the values that your template tags create.

To set a variable in the context, just use dictionary assignment on the context object in the render() method. Here’s an updated version of CurrentTimeNode that sets a template variable current_time instead of outputting it:

import datetime
from django import template

class CurrentTimeNode2(template.Node):
    def __init__(self, format_string):
        self.format_string = format_string
    def render(self, context):
        context['current_time'] = datetime.datetime.now().strftime(self.format_string)
        return ''
Note that render() returns the empty string. render() should always return string output. If all the template tag does is set a variable, render() should return the empty string.

Here’s how you’d use this new version of the tag:

{% current_time "%Y-%m-%d %I:%M %p" %}<p>The time is {{ current_time }}.</p>
Variable scope in context

Any variable set in the context will only be available in the same block of the template in which it was assigned. This behavior is intentional; it provides a scope for variables so that they don’t conflict with context in other blocks.

But, there’s a problem with CurrentTimeNode2: The variable name current_time is hard-coded. This means you’ll need to make sure your template doesn’t use {{ current_time }} anywhere else, because the {% current_time %} will blindly overwrite that variable’s value. A cleaner solution is to make the template tag specify the name of the output variable, like so:

{% current_time "%Y-%m-%d %I:%M %p" as my_current_time %}
<p>The current time is {{ my_current_time }}.</p>
To do that, you’ll need to refactor both the compilation function and Node class, like so:

import re

class CurrentTimeNode3(template.Node):
    def __init__(self, format_string, var_name):
        self.format_string = format_string
        self.var_name = var_name
    def render(self, context):
        context[self.var_name] = datetime.datetime.now().strftime(self.format_string)
        return ''

def do_current_time(parser, token):
    # This version uses a regular expression to parse tag contents.
    try:
        # Splitting by None == splitting by spaces.
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires arguments" % token.contents.split()[0]
        )
    m = re.search(r'(.*?) as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError("%r tag had invalid arguments" % tag_name)
    format_string, var_name = m.groups()
    if not (format_string[0] == format_string[-1] and format_string[0] in ('"', "'")):
        raise template.TemplateSyntaxError(
            "%r tag's argument should be in quotes" % tag_name
        )
    return CurrentTimeNode3(format_string[1:-1], var_name)
The difference here is that do_current_time() grabs the format string and the variable name, passing both to CurrentTimeNode3.

Finally, if you only need to have a simple syntax for your custom context-updating template tag, consider using the simple_tag() shortcut, which supports assigning the tag results to a template variable.

Parsing until another block tag¶
Template tags can work in tandem. For instance, the standard {% comment %} tag hides everything until {% endcomment %}. To create a template tag such as this, use parser.parse() in your compilation function.

Here’s how a simplified {% comment %} tag might be implemented:

def do_comment(parser, token):
    nodelist = parser.parse(('endcomment',))
    parser.delete_first_token()
    return CommentNode()

class CommentNode(template.Node):
    def render(self, context):
        return ''
Note

The actual implementation of {% comment %} is slightly different in that it allows broken template tags to appear between {% comment %} and {% endcomment %}. It does so by calling parser.skip_past('endcomment') instead of parser.parse(('endcomment',)) followed by parser.delete_first_token(), thus avoiding the generation of a node list.

parser.parse() takes a tuple of names of block tags ‘’to parse until’‘. It returns an instance of django.template.NodeList, which is a list of all Node objects that the parser encountered ‘’before’’ it encountered any of the tags named in the tuple.

In "nodelist = parser.parse(('endcomment',))" in the above example, nodelist is a list of all nodes between the {% comment %} and {% endcomment %}, not counting {% comment %} and {% endcomment %} themselves.

After parser.parse() is called, the parser hasn’t yet “consumed” the {% endcomment %} tag, so the code needs to explicitly call parser.delete_first_token().

CommentNode.render() simply returns an empty string. Anything between {% comment %} and {% endcomment %} is ignored.

Parsing until another block tag, and saving contents¶
In the previous example, do_comment() discarded everything between {% comment %} and {% endcomment %}. Instead of doing that, it’s possible to do something with the code between block tags.

For example, here’s a custom template tag, {% upper %}, that capitalizes everything between itself and {% endupper %}.

Usage:

{% upper %}This will appear in uppercase, {{ your_name }}.{% endupper %}
As in the previous example, we’ll use parser.parse(). But this time, we pass the resulting nodelist to the Node:

def do_upper(parser, token):
    nodelist = parser.parse(('endupper',))
    parser.delete_first_token()
    return UpperNode(nodelist)

class UpperNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist
    def render(self, context):
        output = self.nodelist.render(context)
        return output.upper()
The only new concept here is the self.nodelist.render(context) in UpperNode.render().

For more examples of complex rendering, see the source code of {% for %} in django/template/defaulttags.py and {% if %} in django/template/smartif.py.

---
<!-- .slide: data-background="url('images/demo.jpg')" data-background-size="cover" --> 
<!-- .slide: class="lab" -->
## Demo time!
Custom template tags


---
<!-- .slide: data-background="url('images/demo.jpg')" data-background-size="cover" --> 
<!-- .slide: class="lab" -->
## Lab time!
Custom template tags

