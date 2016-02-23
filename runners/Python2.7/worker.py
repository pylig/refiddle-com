import re


class Worker(object):

    FLAG_MAPS = {
        'g': 510,
        's': re.DOTALL,
        'm': re.MULTILINE,
        'l': re.LOCALE,
        'i': re.IGNORECASE,
        'u': re.UNICODE,
        'x': re.VERBOSE,
    }

    REGEXP_IS_CORPUS = re.compile('(\n#[\+\-])')

    def __init__(self, action, pattern, corpus_text, replace_text):
        self.action = action
        self.pattern = pattern
        self.corpus_text = corpus_text
        self.replace_text = replace_text

        self.__is_multi_line = False
        self.__all_groups = 0

        self.__pattern = None
        self.__flags = 0
        self.__flags_str = None

        self.__compiled = None

        self.is_success = None
        self.result = {}

        self.__parse_pattern()
        self.__parse_flags()

        self.__compile_pattern()

        if self.is_success is False:
            return

        self.__action_map = {
            'evaluate': self.__evaluate,
            'replace': self.__replace
        }

        self.run()

    def __parse_pattern(self):
        if self.pattern[0] == '/':
            tmp_pattern = self.pattern.split('/')

            self.__flags_str = tmp_pattern.pop(len(tmp_pattern) - 1)
            self.__pattern = '/'.join(filter(None, tmp_pattern))
        else:
            self.__pattern = self.pattern

    def __parse_flags(self):
        if not self.__flags_str:
            return None

        for flag in self.__flags_str:
            f = self.FLAG_MAPS.get(flag, 0)

            if f == 510:
                self.__is_multi_line = True
                continue

            self.__flags += f

    def __compile_pattern(self):
        try:
            self.__compiled = re.compile(
                self.__pattern,
                flags=self.__flags
            )
        except Exception as exp:
            self.is_success = False
            self.result = {
                'pattern': [str(exp)]
            }

    def __replace(self):
        self.result = {
            'replace': re.sub(
                self.__compiled,
                self.replace_text,
                self.corpus_text
            )
        }

        self.is_success = True

    def __coprus_test(self):
        self.result['matchSummary'] = {
            'total': 0,
            'passing': 0,
            'failed': 0,
            'tests': True
        }

        current = None
        split_text = self.corpus_text.split('\n')

        for text in split_text:
            # text = text.strip()
            if not text:
                continue

            if '#' == text[0]:
                current = text[1]
            else:
                if not current:
                    continue

                result = self.__compiled.match(text)
                start_index = self.corpus_text.index(text)

                if result:
                    end_index = result.span()[1]
                    matching = 'match' if current == '+' else 'nomatch'
                else:
                    end_index = len(text)
                    matching = 'match' if current == '-' else 'nomatch'

                if matching == 'match':
                    self.result['matchSummary']['passing'] += 1
                else:
                    self.result['matchSummary']['failed'] += 1

                self.result['matchSummary']['total'] += 1

                self.result[str(start_index)] = [
                    start_index, end_index, matching]

        self.is_success = True

    def __evaluate(self):
        if self.REGEXP_IS_CORPUS.search(self.corpus_text):
            return self.__coprus_test()

        results = []
        try:
            results = getattr(re, 'search' if not self.__is_multi_line
                              else 'finditer')(
                self.__compiled,
                self.corpus_text
            )
        except Exception as exp:
            self.is_success = False
            self.result = {
                'error': [str(exp)]
            }

        def parse_result(_result):
            if not _result:
                return None

            named_caps = _result.groupdict()
            if named_caps:
                for cap in named_caps:
                    self.result[cap] = (
                        _result.span(cap)[0],
                        _result.span(cap)[1] - _result.span(cap)[0]
                    )

            for group in _result.regs:
                span = (group[0], group[1] - group[0])

                if span in self.result.values():
                    continue

                self.result[self.__all_groups] = span
                self.__all_groups += 1

        if self.__is_multi_line:
            for result in results:
                parse_result(result)
        else:
            parse_result(results)

        self.result['matchSummary'] = {
            'total': len(self.result),
            'tests': False
        }

        self.is_success = True

    def run(self):
        self.__action_map[self.action]()
