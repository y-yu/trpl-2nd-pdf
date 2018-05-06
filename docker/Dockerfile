FROM frolvlad/alpine-glibc:alpine-3.7

MAINTAINER yyu <yyu [at] mental.poker>

ENV TEXLIVE_DEPS \
    xz \
    tar \
    fontconfig-dev
    
ENV TEXLIVE_PATH /usr/local/texlive

ENV PANDOC_DEPS \
    alpine-sdk \
    coreutils \
    ghc \
    gmp \
    libffi \
    linux-headers \
    musl-dev \
    zlib-dev \
    cabal \
    tar

ENV FONT_DEPS \
    unzip \
    fontconfig-dev

ENV FONT_PATH /usr/share/fonts/

ENV PERSISTENT_DEPS \
    python \
    py2-pip \
    wget \
    make \
    perl \
    ghostscript \
    inkscape \
    bash \
    git

ENV PANDOC_VERSION 2.1.3
ENV PANDOC_DOWNLOAD_URL https://hackage.haskell.org/package/pandoc-$PANDOC_VERSION/pandoc-$PANDOC_VERSION.tar.gz
ENV PANDOC_ROOT /usr/local/pandoc

ENV PATH $TEXLIVE_PATH/bin/x86_64-linuxmusl:$PANDOC_ROOT/bin:$PATH

RUN apk upgrade --update

# Install basic dependencies
RUN apk add --no-cache --virtual .persistent-deps $PERSISTENT_DEPS

# Setup fonts
RUN mkdir -p $FONT_PATH && \
    apk add --no-cache --virtual .font-deps $FONT_DEPS && \
    wget https://github.com/adobe-fonts/source-code-pro/archive/2.030R-ro/1.050R-it.zip && \
      unzip 1.050R-it.zip && \
      cp source-code-pro-2.030R-ro-1.050R-it/OTF/*.otf $FONT_PATH && \
      rm -rf 1.050R-it.zip source-code-pro-2.030R-ro-1.050R-it && \
    wget https://github.com/adobe-fonts/source-han-sans/raw/release/SubsetOTF/SourceHanSansJP.zip && \
      unzip SourceHanSansJP.zip && \
      cp SourceHanSansJP/*.otf $FONT_PATH && \
      rm -rf SourceHanSansJP.zip SourceHanSansJP && \
    wget https://github.com/adobe-fonts/source-han-serif/raw/release/SubsetOTF/SourceHanSerifJP.zip && \
      unzip SourceHanSerifJP.zip && \
      cp SourceHanSerifJP/*.otf $FONT_PATH && \
      rm -rf SourceHanSerifJP.zip SourceHanSerifJP && \
    fc-cache -f -v && \
    apk del .font-deps 

# Install Pandoc
# See https://github.com/skyzyx/alpine-pandoc/blob/master/Dockerfile
RUN apk add --no-cache --virtual .pandoc-deps $PANDOC_DEPS  && \
    apk add --no-cache --virtual .cabal cabal -X http://dl-cdn.alpinelinux.org/alpine/edge/community && \
    wget -qO- "$PANDOC_DOWNLOAD_URL" | tar -xzf - && \
      ( cd pandoc-$PANDOC_VERSION && cabal update && cabal install --only-dependencies && \
      cabal configure --prefix=$PANDOC_ROOT && \
      cabal build && \
      cabal copy && \
      cd .. ) && \
    rm -Rf pandoc-$PANDOC_VERSION/ && \
    rm -Rf /root/.cabal/ /root/.ghc/ && \
    apk del .pandoc-deps .cabal

# Install Pandocfilter
COPY requirements.txt ./
RUN pip install --user --upgrade pip && \
    pip install --user -r requirements.txt && \
    rm requirements.txt

# Install TeXLive
RUN apk add --no-cache --no-cache --virtual .texlive-deps $TEXLIVE_DEPS && \
    mkdir /tmp/install-tl-unx && \
    wget -qO- http://mirror.ctan.org/systems/texlive/tlnet/install-tl-unx.tar.gz | \
      tar -xz -C /tmp/install-tl-unx --strip-components=1 && \
    printf "%s\n" \
      "TEXDIR $TEXLIVE_PATH" \
      "selected_scheme scheme-small" \
      "option_doc 0" \
      "option_src 0" \
      > /tmp/install-tl-unx/texlive.profile && \
    /tmp/install-tl-unx/install-tl \
      --profile=/tmp/install-tl-unx/texlive.profile && \
    tlmgr install latexmk collection-luatex collection-langjapanese \
      collection-fontsrecommended type1cm mdframed needspace fncychap \
      everyhook svn-prov enumitem && \
    rm -fr /tmp/install-tl-unx && \
    apk del .texlive-deps

VOLUME ["/workdir"]

WORKDIR /workdir

ENTRYPOINT ["/bin/bash", "-c", "./setup.sh && USE_SOURCEHAN=true make"]
