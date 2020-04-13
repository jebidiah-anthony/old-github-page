find ./ -name "*.adoc" 2>/dev/null | sed -e 's/\(.*\)adoc/rm \1html 2>\/dev\/null/g' > /tmp/build_jekyll.sh

sh /tmp/build_jekyll.sh

bundle exec jekyll build

find ./ -name "*.adoc" 2>/dev/null | sed -e 's/.\/\(.*\).adoc/mv _site\/\1.html \1.html/g' > /tmp/build_jekyll.sh

sh /tmp/build_jekyll.sh

rm -rf _site/
rm -rf .jekyll-cache/
