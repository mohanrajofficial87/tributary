import tributary.streaming as ts
import pytest


class TestPostgres:
    @pytest.mark.skipif("sys.platform != 'linux'")
    def test_http(self):
        query = ['SELECT * FROM test']
        out = ts.PostgresSource(queries=query,
                          user='postgres',
                          database='postgres',
                          password='test',
                          host='localhost:5432')
        assert len(ts.run(out)) != 0