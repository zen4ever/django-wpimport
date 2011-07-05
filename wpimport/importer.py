from __future__ import with_statement

from datetime import datetime
from BeautifulSoup import BeautifulStoneSoup


class BaseWordpressImporter(object):

    default_mapping = [
        ('title', 'title'),
        ('dc:creator', 'creator'),
        ('description', 'description'),
        ('content:encoded', 'content'),
        ('wp:post_id', ('post_id', 'convert_int')),
        ('wp:post_date', ('post_date', 'convert_date')),
        ('wp:post_date_gmt', ('post_date_gmt', 'convert_date')),
        ('wp:comment_status', 'comment_status'),
        ('wp:post_name', 'slug'),
        ('wp:status', 'status'),
        ('wp:post_parent', 'parent'),
        ('excerpt:encoded', 'excerpt'),
        ('wp:postmeta', ('postmeta', 'convert_meta', 'dict')),
        ('category', ('categories', 'convert_category', 'list')),
        ('wp:comment', ('comments', 'convert_comment', 'list')),
        ('wp:post_type', 'post_type'),
        ('wp:attachment_url', 'attachment_url'),
        ('wp:ping_status', 'ping_status'),
        ('wp:menu_order', ('menu_order', 'convert_int')),
        ('wp:post_password', 'post_password'),
        ('wp:is_sticky', ('is_sticky', 'convert_bool')),
        ('link', 'link'),
        ('pubdate', 'pubdate'),
        ('guid', ('guid', 'convert_guid')),

        ('wp:tag_slug', 'tag_slug'),
        ('wp:tag_name', 'tag_name'),
        ('wp:term_id', ('term_id', 'convert_int')),
        ('wp:term_parent', 'term_parent'),
        ('wp:term_taxonomy', 'term_taxonomy'),
        ('wp:term_slug', 'term_slug'),
        ('wp:term_name', 'term_name'),

        ('wp:cat_name', 'category_name'),
        ('wp:category_nicename', 'category_slug'),
        ('wp:category_parent', 'category_parent'),

        ('wp:comment_id', ('id', 'convert_int')),
        ('wp:comment_author', 'author'),
        ('wp:comment_author_email', 'author_email'),
        ('wp:comment_author_url', 'author_url'),
        ('wp:comment_author_ip', 'author_ip'),
        ('wp:comment_date', ('date', 'convert_date')),
        ('wp:comment_date_gmt', ('date_gmt', 'convert_date')),
        ('wp:comment_content', 'content'),
        ('wp:comment_approved', ('approved', 'convert_bool')),
        ('wp:comment_parent', ('parent', 'convert_int')),
        ('wp:comment_user_id', ('user_id', 'convert_int')),
        ('wp:comment_type', 'type'),
        ('wp:author_id', ('author_id', 'convert_int')),
        ('wp:author_login', 'author_login'),
        ('wp:author_email', 'author_email'),
        ('wp:author_display_name', 'author_display_name'),
        ('wp:author_first_name', 'author_first_name'),
        ('wp:author_last_name', 'author_last_name'),
    ]

    def __init__(self, filename, verbosity=0):
        self.verbosity = verbosity
        with open(filename) as fh:
            self.xml = BeautifulStoneSoup(fh.read())

    def convert_int(self, tag):
        return int(tag.string)

    def convert_bool(self, tag):
        return bool(int(tag.string))

    def convert_guid(self, tag):
        return {'is_permalink': tag['ispermalink'] == 'true', 'guid': tag.string}

    def convert_date(self, tag):
        try:
            return datetime.strptime(tag.string, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return None

    def convert_meta(self, tag):
        key = tag.find('wp:meta_key').string
        value = tag.find('wp:meta_value').string
        return (key, value)

    def convert_category(self, tag):
        return {
            'slug': tag['nicename'],
            'name': tag.string,
            'domain': tag['domain'],
        }

    def convert_comment(self, tag):
        return self.handle_tag(tag, dict(self.default_mapping))

    def parse(self):
        items = self.xml.findAll(lambda x: x.parent.name == 'channel')
        for item in items:
            post_type = item.find('wp:post_type') and item.find('wp:post_type').string
            if post_type and hasattr(self, 'handle_' + post_type):
                getattr(self, 'handle_' + post_type)(item)
            else:
                self.handle_default(item)

    def handle_tag(self, tag, mapping):
        result = {}
        children = tag.findAll(lambda x: x.parent == tag)
        for child in children:
            attr = mapping.get(child.name, None)
            if attr:
                if isinstance(attr, str):
                    result[attr] = child.string
                elif isinstance(attr, tuple):
                    if len(attr) == 2:
                        attr_name, converter = attr
                        attr_type = None
                    elif len(attr) == 3:
                        attr_name, converter, attr_type = attr
                    if isinstance(converter, str):
                        converter = getattr(self, converter)
                    value = converter(child)
                    if attr_type == 'list':
                        attr_value = result.get(attr_name, [])
                        attr_value.append(value)
                        result[attr_name] = attr_value
                    elif attr_type == 'dict':
                        attr_value = result.get(attr_name, {})
                        attr_value[value[0]] = value[1]
                        result[attr_name] = attr_value
                    else:
                        result[attr_name] = value
            elif self.verbosity > 0:
                print "No match: ", child
        return result

    def handle_default(self, tag):
        mp = dict(self.default_mapping)
        result = self.handle_tag(tag, mp)
        if not result:
            result = dict([(tag.name, tag.string)])
        if self.verbosity > 1:
            from pprint import pprint
            pprint(result)
        return result
