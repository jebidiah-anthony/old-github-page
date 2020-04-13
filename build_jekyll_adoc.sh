find ./ -name "*.adoc" 2>/dev/null | sed -e 's/\(.*\)adoc/rm \1html 2>\/dev\/null/g' > /tmp/build_jekyll.sh

sh /tmp/build_jekyll.sh

bundle exec jekyll build
