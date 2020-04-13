find ./ -name "*.adoc" 2>/dev/null | sed -e 's/.\/\(.*\).adoc/mv _site\/\1.html \1.html/g' > /tmp/move_adoc.sh

sh /tmp/move_adoc.sh

rm -rf _site/
rm -rf .jekyll-cache/
